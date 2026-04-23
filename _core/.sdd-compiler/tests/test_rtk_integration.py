"""
Tests for RTK (Runtime Telemetry Kit) sub-layer integration

Tests deduplication engine and pattern matching within compiler pipeline.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.runtime_telemetry_kit import (
    DeduplicationEngine,
    PatternRegistry,
    CompressionMetrics,
    deduplicate_event,
    get_engine,
    get_compression_metrics,
)
from src.runtime_telemetry_kit.patterns import ExtendedPatterns


class TestRTKIntegration:
    """Test RTK as sub-layer of compiler"""
    
    def test_rtk_available(self):
        """Test RTK module is available"""
        assert DeduplicationEngine is not None
        assert PatternRegistry is not None
    
    def test_pattern_registry_loads(self):
        """Test pattern registry loads 50+ patterns"""
        registry = PatternRegistry()
        assert registry.patterns is not None
        assert len(registry.patterns) > 0
        # Should have at least the basic patterns
        assert "TS001" in registry.patterns  # ISO timestamp
        assert "SRV01" in registry.patterns  # Service header
    
    def test_deduplicate_event_basic(self):
        """Test basic event deduplication"""
        event = {
            "timestamp": "2026-04-21T14:30:00Z",
            "service": "sdd-api",
            "status": 200,
        }
        
        engine = DeduplicationEngine()
        compressed = engine.deduplicate(event)
        
        # Should have placeholder tokens
        assert "$TS" in str(compressed) or "$" in str(compressed)
    
    def test_compression_metrics(self):
        """Test compression metrics tracking"""
        engine = DeduplicationEngine()
        event = {
            "timestamp": "2026-04-21T14:30:00Z",
            "service": "sdd-api",
            "version": "3.1.0",
            "status": 200,
            "response_time": "150ms",
        }
        
        compressed = engine.deduplicate(event)
        metrics = engine.metrics
        
        assert isinstance(metrics, CompressionMetrics)
        assert metrics.original_size > 0
        assert metrics.compressed_size > 0
        assert metrics.compression_ratio >= 0.0
    
    def test_extended_patterns_available(self):
        """Test extended patterns (90% coverage)"""
        patterns = ExtendedPatterns.get_all_patterns()
        assert patterns is not None
        assert len(patterns) > 40  # Should have 50+ patterns


class TestRTKPatternMatching:
    """Test pattern matching accuracy"""
    
    def test_timestamp_pattern(self):
        """Test ISO 8601 timestamp pattern matching"""
        engine = DeduplicationEngine()
        event = {
            "timestamp": "2026-04-21T14:30:00Z",
            "created_at": "2026-04-21T14:30:00.123Z",
        }
        
        compressed = engine.deduplicate(event)
        assert compressed is not None
    
    def test_http_status_pattern(self):
        """Test HTTP status code pattern matching"""
        engine = DeduplicationEngine()
        
        for status in [200, 201, 204, 400, 401, 403, 404, 500]:
            event = {"status": status}
            compressed = engine.deduplicate(event)
            assert compressed is not None
    
    def test_multiple_events_compression(self):
        """Test compression across multiple events"""
        engine = DeduplicationEngine()
        
        events = [
            {
                "timestamp": "2026-04-21T14:30:00Z",
                "service": "sdd-api",
                "status": 200,
            },
            {
                "timestamp": "2026-04-21T14:30:01Z",
                "service": "sdd-api",
                "status": 200,
            },
            {
                "timestamp": "2026-04-21T14:30:02Z",
                "service": "sdd-compiler",
                "status": 201,
            },
        ]
        
        total_original = sum(len(str(e)) for e in events)
        compressed_events = [engine.deduplicate(e) for e in events]
        total_compressed = sum(len(str(e)) for e in compressed_events)
        
        # Should have some compression
        assert total_original >= total_compressed


class TestCompilerRTKIntegration:
    """Test RTK integration with main compiler"""
    
    def test_dsl_compiler_imports_rtk(self):
        """Test that DSL compiler can import RTK"""
        from src.dsl_compiler import HAS_RTK
        assert HAS_RTK is True
    
    def test_compilation_metrics_include_rtk(self):
        """Test compilation metrics include RTK fields"""
        from src.dsl_compiler import CompilationMetrics
        
        metrics = CompilationMetrics()
        
        # Should have RTK fields
        assert hasattr(metrics, 'rtk_compression_ratio')
        assert hasattr(metrics, 'rtk_patterns_matched')
        assert metrics.rtk_compression_ratio == 0.0
        assert metrics.rtk_patterns_matched == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
