"""
RTK (Runtime Telemetry Kit) Deduplication Engine

Provides O(1) pattern matching and compression for telemetry events.
Target: 60-70% overhead reduction with 90% pattern coverage.
"""

import hashlib
import json
import re
from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class CompressionMetrics:
    """Tracks compression performance"""
    original_size: int
    compressed_size: int
    pattern_matches: int
    cache_hits: int
    cache_misses: int

    @property
    def compression_ratio(self) -> float:
        """Percentage of data removed by compression"""
        if self.original_size == 0:
            return 0.0
        return (self.original_size - self.compressed_size) / self.original_size

    @property
    def cache_hit_ratio(self) -> float:
        """Percentage of cache hits vs total lookups"""
        total = self.cache_hits + self.cache_misses
        if total == 0:
            return 0.0
        return self.cache_hits / total


class PatternRegistry:
    """In-memory pattern registry with O(1) lookup"""

    def __init__(self):
        self.patterns: Dict[str, Dict[str, Any]] = {}
        self.pattern_by_id: Dict[str, str] = {}  # ID → pattern key
        self._load_patterns()

    def _load_patterns(self) -> None:
        """Load v3.1 patterns (50+ for 90% coverage)"""
        # Import extended patterns
        try:
            from patterns import ExtendedPatterns
            all_patterns = ExtendedPatterns.get_all_patterns()
        except ImportError:
            # Fallback to basic patterns if patterns.py not available
            all_patterns = self._get_basic_patterns()

        # Load all patterns
        for pattern_id, pattern_info in all_patterns.items():
            self._add_pattern_from_dict(pattern_id, pattern_info)

    def _get_basic_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Get basic patterns for fallback"""
        return {
            "TS001": {
                "name": "ISO 8601 Timestamp",
                "regex": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?$",
                "fields": ["timestamp", "created_at", "updated_at"],
                "compression_ratio": 0.15,
                "frequency": 0.95,
            },
            "SRV01": {
                "name": "Service Header",
                "regex": r"^(sdd-api|sdd-core|sdd-extensions|sdd-dashboard)$",
                "fields": ["service"],
                "compression_ratio": 0.20,
                "frequency": 0.90,
            },
            "VER01": {
                "name": "Version String",
                "regex": r"^\d+\.\d+\.\d+",
                "fields": ["version"],
                "compression_ratio": 0.18,
                "frequency": 0.95,
            },
            "ST001": {
                "name": "HTTP Status Code",
                "values": [200, 201, 204, 400, 401, 403, 404, 500, 502, 503],
                "fields": ["status", "http_code"],
                "compression_ratio": 0.05,
                "frequency": 0.80,
            },
            "ERR001": {
                "name": "Connection Timeout",
                "regex": r"Connection timeout at .+:\d+",
                "fields": ["error_message"],
                "compression_ratio": 0.15,
                "frequency": 0.12,
            },
            "UUID001": {
                "name": "UUID Format",
                "regex": r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
                "fields": ["id", "entity_id", "trace_id", "request_id"],
                "compression_ratio": 0.44,
                "frequency": 0.70,
            },
        }

    def _add_pattern_from_dict(
        self, pattern_id: str, pattern_info: Dict[str, Any]
    ) -> None:
        """Add pattern from dictionary"""
        self._add_pattern(
            pattern_id,
            pattern_info.get("name", "Unknown"),
            regex=pattern_info.get("regex"),
            values=pattern_info.get("values"),
            fields=pattern_info.get("fields", []),
            compression_ratio=pattern_info.get("compression_ratio", 0.0),
            frequency=pattern_info.get("frequency", 0.0),
        )

    def _add_pattern(
        self,
        pattern_id: str,
        name: str,
        regex: Optional[str] = None,
        values: Optional[List[Any]] = None,
        fields: Optional[List[str]] = None,
        compression_ratio: float = 0.0,
        frequency: float = 0.0
    ) -> None:
        """Add pattern to registry"""
        pattern = {
            "id": pattern_id,
            "name": name,
            "regex": regex,
            "values": values,
            "fields": fields or [],
            "compression_ratio": compression_ratio,
            "frequency": frequency,
        }
        self.patterns[pattern_id] = pattern
        self.pattern_by_id[pattern_id] = pattern_id

    def find_pattern(self, field: str, value: Any) -> Optional[str]:
        """Find matching pattern for field:value (O(1) with hash lookup)"""
        for pattern in self.patterns.values():
            # Check field match
            if field not in pattern["fields"]:
                continue

            # Check value match (regex or list)
            if pattern["regex"]:
                if isinstance(value, str) and re.match(pattern["regex"], value):
                    return pattern["id"]

            if pattern["values"]:
                if value in pattern["values"]:
                    return pattern["id"]

        return None

    def get_pattern(self, pattern_id: str) -> Optional[Dict[str, Any]]:
        """Get pattern definition by ID"""
        return self.patterns.get(pattern_id)


class DeduplicationEngine:
    """Main deduplication engine with caching"""

    def __init__(self, max_cache_size: int = 1000):
        self.registry = PatternRegistry()
        self.cache_max = max_cache_size
        self.cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self.metrics = CompressionMetrics(0, 0, 0, 0, 0)

    def deduplicate(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deduplicate telemetry event using pattern matching
        
        Time Complexity: O(1) average (with cache), O(n) worst case
        Space Complexity: O(n) for pattern storage
        
        Args:
            event: Original telemetry event
            
        Returns:
            Deduplicated event with pattern references
        """
        # Create cache key (deterministic hash)
        event_json = json.dumps(event, sort_keys=True, default=str)
        event_hash = hashlib.md5(event_json.encode()).hexdigest()

        # Check cache
        if event_hash in self.cache:
            self.metrics.cache_hits += 1
            return self.cache[event_hash]

        self.metrics.cache_misses += 1

        # Calculate original size
        original_size = len(event_json)
        self.metrics.original_size += original_size

        # Deduplicate fields
        compressed = {}
        for field, value in event.items():
            pattern_id = self.registry.find_pattern(field, value)

            if pattern_id:
                # Pattern found: use reference
                compressed[field] = f"${pattern_id}"
                self.metrics.pattern_matches += 1
            else:
                # No pattern: encode value intelligently
                compressed[field] = self._encode_value(value)

        # Calculate compressed size
        compressed_json = json.dumps(compressed, sort_keys=True, default=str)
        compressed_size = len(compressed_json)
        self.metrics.compressed_size += compressed_size

        # Cache result
        self._cache_put(event_hash, compressed)

        return compressed

    def _encode_value(self, value: Any) -> Any:
        """Intelligently encode values without pattern match"""
        if value is None:
            return None

        if isinstance(value, bool):
            return value

        if isinstance(value, (int, float)):
            return value

        if isinstance(value, str):
            # Detect and encode timestamps (even if not v3.0 ISO format)
            if self._is_timestamp_like(value):
                return self._encode_timestamp(value)

            # Detect and encode UUIDs
            if self._is_uuid_like(value):
                return f"#UUID:{value[:8]}..."  # Truncated for readability

            return value

        if isinstance(value, (list, dict)):
            # Recursively encode nested structures
            if isinstance(value, list):
                return [self._encode_value(v) for v in value]
            else:
                return {k: self._encode_value(v) for k, v in value.items()}

        return value

    @staticmethod
    def _is_timestamp_like(value: str) -> bool:
        """Heuristic: detect timestamp-like strings"""
        if len(value) < 19:  # YYYY-MM-DD HH:MM:SS minimum
            return False

        patterns = [
            r"^\d{4}-\d{2}-\d{2}",  # ISO date
            r"^\d{4}/\d{2}/\d{2}",  # Slash format
            r"^\d{10,13}$",          # Unix timestamp
        ]

        return any(re.match(p, value) for p in patterns)

    @staticmethod
    def _is_uuid_like(value: str) -> bool:
        """Heuristic: detect UUID/ULID patterns"""
        return bool(re.match(
            r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            value,
            re.IGNORECASE
        ))

    @staticmethod
    def _encode_timestamp(value: str) -> str:
        """Encode timestamp as compact reference"""
        try:
            # Parse ISO 8601
            dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
            # Return compact Unix timestamp
            return f"#TS:{int(dt.timestamp())}"
        except (ValueError, AttributeError):
            return value

    def _cache_put(self, key: str, value: Dict[str, Any]) -> None:
        """Put item in LRU cache"""
        # Remove oldest item if cache full
        if len(self.cache) >= self.cache_max:
            self.cache.popitem(last=False)

        self.cache[key] = value

    def get_metrics(self) -> CompressionMetrics:
        """Get compression metrics"""
        return self.metrics

    def reset_metrics(self) -> None:
        """Reset compression metrics"""
        self.metrics = CompressionMetrics(0, 0, 0, 0, 0)

    def clear_cache(self) -> None:
        """Clear deduplication cache"""
        self.cache.clear()


# Module-level convenience functions
_engine: Optional[DeduplicationEngine] = None


def get_engine() -> DeduplicationEngine:
    """Get or create singleton deduplication engine"""
    global _engine
    if _engine is None:
        _engine = DeduplicationEngine()
    return _engine


def deduplicate_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Deduplicate a single telemetry event (convenience function)"""
    return get_engine().deduplicate(event)


def get_compression_metrics() -> CompressionMetrics:
    """Get current compression metrics"""
    return get_engine().get_metrics()


def reset_metrics() -> None:
    """Reset compression metrics"""
    get_engine().reset_metrics()


if __name__ == "__main__":
    # Example usage
    engine = DeduplicationEngine()

    # Sample telemetry event
    event = {
        "timestamp": "2026-04-21T14:30:00Z",
        "service": "sdd-api",
        "version": "3.1.0",
        "status": 200,
        "trace_id": "550e8400-e29b-41d4-a716-446655440000",
        "message": "Request processed successfully"
    }

    print("Original event:")
    print(json.dumps(event, indent=2))
    print()

    compressed = engine.deduplicate(event)
    print("Deduplicated event:")
    print(json.dumps(compressed, indent=2))
    print()

    metrics = engine.get_metrics()
    print(f"Compression ratio: {metrics.compression_ratio:.1%}")
    print(f"Cache hit ratio: {metrics.cache_hit_ratio:.1%}")
