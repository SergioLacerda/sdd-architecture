"""
Tests for RTK Deduplication Engine

Coverage:
- Pattern matching
- Caching behavior
- Compression metrics
- Edge cases and error handling
"""

import pytest
import json
from datetime import datetime
from .engine import (
    DeduplicationEngine,
    PatternRegistry,
    CompressionMetrics,
    deduplicate_event,
    get_engine,
    reset_metrics,
)


class TestPatternRegistry:
    """Test pattern matching and registry"""
    
    def test_timestamp_pattern_detection(self):
        """Test ISO 8601 timestamp pattern matching"""
        registry = PatternRegistry()
        pattern_id = registry.find_pattern("timestamp", "2026-04-21T14:30:00Z")
        assert pattern_id == "TS001"
    
    def test_service_pattern_detection(self):
        """Test service name pattern matching"""
        registry = PatternRegistry()
        pattern_id = registry.find_pattern("service", "sdd-api")
        assert pattern_id == "SRV01"
    
    def test_version_pattern_detection(self):
        """Test version string pattern matching"""
        registry = PatternRegistry()
        pattern_id = registry.find_pattern("version", "3.1.0")
        assert pattern_id == "VER01"
    
    def test_status_code_pattern_detection(self):
        """Test HTTP status code pattern matching"""
        registry = PatternRegistry()
        
        # Valid status codes
        for status in [200, 201, 400, 404, 500]:
            pattern_id = registry.find_pattern("status", status)
            assert pattern_id == "ST001"
        
        # Invalid status code
        pattern_id = registry.find_pattern("status", 999)
        assert pattern_id is None
    
    def test_uuid_pattern_detection(self):
        """Test UUID pattern matching"""
        registry = PatternRegistry()
        pattern_id = registry.find_pattern("trace_id", "550e8400-e29b-41d4-a716-446655440000")
        assert pattern_id == "UUID001"
    
    def test_non_matching_field(self):
        """Test field that doesn't match any pattern"""
        registry = PatternRegistry()
        pattern_id = registry.find_pattern("unknown_field", "random_value")
        assert pattern_id is None
    
    def test_pattern_lookup_by_id(self):
        """Test pattern retrieval by ID"""
        registry = PatternRegistry()
        pattern = registry.get_pattern("TS001")
        
        assert pattern is not None
        assert pattern["id"] == "TS001"
        assert pattern["name"] == "ISO 8601 Timestamp"
        assert pattern["regex"] is not None


class TestDeduplicationEngine:
    """Test deduplication engine core functionality"""
    
    def test_simple_timestamp_deduplication(self):
        """Test deduplication of single timestamp field"""
        engine = DeduplicationEngine()
        
        event = {
            "timestamp": "2026-04-21T14:30:00Z",
            "message": "Test"
        }
        
        compressed = engine.deduplicate(event)
        
        assert compressed["timestamp"] == "$TS001"
        assert compressed["message"] == "Test"
    
    def test_multiple_field_deduplication(self):
        """Test deduplication of multiple fields"""
        engine = DeduplicationEngine()
        
        event = {
            "timestamp": "2026-04-21T14:30:00Z",
            "service": "sdd-api",
            "version": "3.1.0",
            "status": 200
        }
        
        compressed = engine.deduplicate(event)
        
        assert compressed["timestamp"] == "$TS001"
        assert compressed["service"] == "$SRV01"
        assert compressed["version"] == "$VER01"
        assert compressed["status"] == "$ST001"
    
    def test_uuid_deduplication(self):
        """Test UUID pattern matching and deduplication"""
        engine = DeduplicationEngine()
        
        event = {
            "trace_id": "550e8400-e29b-41d4-a716-446655440000"
        }
        
        compressed = engine.deduplicate(event)
        
        assert compressed["trace_id"] == "$UUID001"
    
    def test_mixed_pattern_and_no_pattern_fields(self):
        """Test mix of fields with and without patterns"""
        engine = DeduplicationEngine()
        
        event = {
            "timestamp": "2026-04-21T14:30:00Z",
            "user_name": "alice",
            "status": 200,
            "description": "Request completed"
        }
        
        compressed = engine.deduplicate(event)
        
        assert compressed["timestamp"] == "$TS001"
        assert compressed["user_name"] == "alice"  # No pattern
        assert compressed["status"] == "$ST001"
        assert compressed["description"] == "Request completed"  # No pattern
    
    def test_nested_structure_deduplication(self):
        """Test deduplication of nested objects"""
        engine = DeduplicationEngine()
        
        event = {
            "timestamp": "2026-04-21T14:30:00Z",
            "metadata": {
                "service": "sdd-api",
                "version": "3.1.0"
            }
        }
        
        compressed = engine.deduplicate(event)
        
        assert compressed["timestamp"] == "$TS001"
        assert compressed["metadata"]["service"] == "$SRV01"
        assert compressed["metadata"]["version"] == "$VER01"
    
    def test_list_deduplication(self):
        """Test deduplication of list items"""
        engine = DeduplicationEngine()
        
        event = {
            "timestamps": [
                "2026-04-21T14:30:00Z",
                "2026-04-21T14:31:00Z"
            ]
        }
        
        compressed = engine.deduplicate(event)
        
        # List items should be deduplicated
        assert all(ts == "$TS001" for ts in compressed["timestamps"])


class TestCaching:
    """Test caching behavior"""
    
    def test_cache_hit_on_duplicate_event(self):
        """Test that cache hits occur for identical events"""
        engine = DeduplicationEngine()
        engine.reset_metrics()
        
        event = {
            "timestamp": "2026-04-21T14:30:00Z",
            "service": "sdd-api"
        }
        
        # First call (cache miss)
        compressed1 = engine.deduplicate(event)
        metrics1 = engine.get_metrics()
        assert metrics1.cache_misses == 1
        assert metrics1.cache_hits == 0
        
        # Second call (cache hit)
        compressed2 = engine.deduplicate(event)
        metrics2 = engine.get_metrics()
        assert metrics2.cache_misses == 1
        assert metrics2.cache_hits == 1
        
        # Results should be identical
        assert compressed1 == compressed2
    
    def test_cache_size_limit(self):
        """Test that cache respects size limit"""
        engine = DeduplicationEngine(max_cache_size=3)
        
        # Add 5 different events (exceeds cache size)
        events = [
            {"timestamp": f"2026-04-21T14:{i:02d}:00Z"}
            for i in range(5)
        ]
        
        for event in events:
            engine.deduplicate(event)
        
        # Cache should not exceed max size
        assert len(engine.cache) <= 3
    
    def test_cache_clear(self):
        """Test cache clearing"""
        engine = DeduplicationEngine()
        
        event = {"timestamp": "2026-04-21T14:30:00Z"}
        engine.deduplicate(event)
        
        assert len(engine.cache) > 0
        
        engine.clear_cache()
        
        assert len(engine.cache) == 0


class TestCompressionMetrics:
    """Test compression metrics calculation"""
    
    def test_compression_ratio_calculation(self):
        """Test compression ratio metric"""
        metrics = CompressionMetrics(
            original_size=256,
            compressed_size=64,
            pattern_matches=4,
            cache_hits=5,
            cache_misses=1
        )
        
        # 256 -> 64 = 75% reduction
        assert metrics.compression_ratio == 0.75
    
    def test_cache_hit_ratio_calculation(self):
        """Test cache hit ratio metric"""
        metrics = CompressionMetrics(
            original_size=100,
            compressed_size=25,
            pattern_matches=3,
            cache_hits=8,
            cache_misses=2
        )
        
        # 8 hits / 10 total = 80%
        assert metrics.cache_hit_ratio == 0.8
    
    def test_zero_division_protection(self):
        """Test metrics handle zero values gracefully"""
        metrics = CompressionMetrics(0, 0, 0, 0, 0)
        
        assert metrics.compression_ratio == 0.0
        assert metrics.cache_hit_ratio == 0.0


class TestValueEncoding:
    """Test intelligent value encoding"""
    
    def test_timestamp_encoding(self):
        """Test timestamp value encoding"""
        engine = DeduplicationEngine()
        
        # Even timestamps without exact pattern match should be encoded
        encoded = engine._encode_value("2026-04-21T14:30:00Z")
        assert isinstance(encoded, str)
    
    def test_uuid_encoding(self):
        """Test UUID value encoding"""
        engine = DeduplicationEngine()
        
        uuid_val = "550e8400-e29b-41d4-a716-446655440000"
        encoded = engine._encode_value(uuid_val)
        
        assert isinstance(encoded, str)
        assert "UUID" in encoded or uuid_val in encoded
    
    def test_numeric_values_preserved(self):
        """Test numeric values are preserved"""
        engine = DeduplicationEngine()
        
        assert engine._encode_value(42) == 42
        assert engine._encode_value(3.14) == 3.14
        assert engine._encode_value(0) == 0
    
    def test_boolean_values_preserved(self):
        """Test boolean values are preserved"""
        engine = DeduplicationEngine()
        
        assert engine._encode_value(True) is True
        assert engine._encode_value(False) is False
    
    def test_none_value_preserved(self):
        """Test None values are preserved"""
        engine = DeduplicationEngine()
        
        assert engine._encode_value(None) is None


class TestModuleFunctions:
    """Test module-level convenience functions"""
    
    def test_deduplicate_event_function(self):
        """Test module-level deduplicate_event function"""
        event = {
            "timestamp": "2026-04-21T14:30:00Z",
            "service": "sdd-api"
        }
        
        compressed = deduplicate_event(event)
        
        assert compressed["timestamp"] == "$TS001"
        assert compressed["service"] == "$SRV01"
    
    def test_get_engine_singleton(self):
        """Test get_engine returns singleton"""
        engine1 = get_engine()
        engine2 = get_engine()
        
        assert engine1 is engine2
    
    def test_reset_metrics_function(self):
        """Test module-level reset_metrics function"""
        # Generate some metrics
        deduplicate_event({"timestamp": "2026-04-21T14:30:00Z"})
        
        # Reset
        reset_metrics()
        
        metrics = get_engine().get_metrics()
        assert metrics.original_size == 0
        assert metrics.compressed_size == 0


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_event(self):
        """Test deduplication of empty event"""
        engine = DeduplicationEngine()
        
        compressed = engine.deduplicate({})
        
        assert compressed == {}
    
    def test_very_large_event(self):
        """Test deduplication of large event"""
        engine = DeduplicationEngine()
        
        event = {
            f"field_{i}": f"2026-04-21T14:{i%60:02d}:00Z"
            for i in range(1000)
        }
        
        compressed = engine.deduplicate(event)
        
        # All should be deduplicated
        assert all(v == "$TS001" for v in compressed.values())
    
    def test_special_characters_in_values(self):
        """Test handling of special characters"""
        engine = DeduplicationEngine()
        
        event = {
            "message": "Error: Connection failed at server:port",
            "description": "Special chars: @#$%^&*()"
        }
        
        compressed = engine.deduplicate(event)
        
        # Should preserve special characters
        assert "@" in compressed["description"]
        assert "$" in compressed["description"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
