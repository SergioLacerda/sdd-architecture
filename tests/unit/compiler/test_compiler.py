"""
Tests for DSL Compiler

Tests parsing, compilation, and metrics generation.
"""

import json
import tempfile
from pathlib import Path

import pytest
from sdd_compiler.dsl_compiler import (
    CompilationMetrics,
    DSLCompiler,
    DSLParser,
    DSLValidator,
    StringPool,
    compile_file,
    compile_string,
)


class TestDSLValidator:
    """Test DSL validation"""

    def test_valid_mandate_syntax(self):
        """Test valid mandate syntax passes validation"""
        dsl = """
        mandate M001 {
          type: HARD
          title: "Test Mandate"
          description: "Test description"
          category: general
        }
        """
        errors = DSLValidator.validate_dsl(dsl)
        assert len(errors) == 0

    def test_mandate_id_must_be_sequential(self):
        """Test mandate IDs must be sequential"""
        dsl = """
        mandate M001 {
          type: HARD
          title: "First"
          description: "Test"
        }
        mandate M003 {
          type: HARD
          title: "Third"
          description: "Test"
        }
        """
        errors = DSLValidator.validate_dsl(dsl)
        assert any("not sequential" in e for e in errors)

    def test_mandate_missing_required_field(self):
        """Test mandate must have required fields"""
        dsl = """
        mandate M001 {
          title: "Test"
          description: "Test"
        }
        """
        errors = DSLValidator.validate_dsl(dsl)
        assert any("missing field" in e for e in errors)

    def test_valid_guideline_syntax(self):
        """Test valid guideline syntax passes validation"""
        dsl = """
        guideline G01 {
          type: SOFT
          title: "Test Guideline"
          description: "Test description"
          category: general
        }
        """
        errors = DSLValidator.validate_dsl(dsl)
        assert len(errors) == 0

    def test_guideline_id_must_be_sequential(self):
        """Test guideline IDs must be sequential"""
        dsl = """
        guideline G01 {
          type: SOFT
          title: "First"
          description: "Test"
        }
        guideline G03 {
          type: SOFT
          title: "Third"
          description: "Test"
        }
        """
        errors = DSLValidator.validate_dsl(dsl)
        assert any("not sequential" in e for e in errors)


class TestDSLParser:
    """Test DSL parsing"""

    def test_parse_simple_mandate(self):
        """Test parsing simple mandate"""
        dsl = """
        mandate M001 {
          type: HARD
          title: "Clean Architecture"
          description: "Applications MUST..."
          category: architecture
        }
        """
        mandates = DSLParser.parse_mandates(dsl)

        assert len(mandates) == 1
        assert mandates[0]["id"] == "M001"
        assert mandates[0]["type"] == "HARD"
        assert mandates[0]["title"] == "Clean Architecture"
        assert mandates[0]["category"] == "architecture"

    def test_parse_mandate_with_validation(self):
        """Test parsing mandate with validation commands"""
        dsl = """
        mandate M001 {
          type: HARD
          title: "Test"
          description: "Test"
          validation: {
            commands: ["pytest", "coverage"]
          }
        }
        """
        mandates = DSLParser.parse_mandates(dsl)

        assert len(mandates) == 1
        assert mandates[0]["validation_commands"] == ["pytest", "coverage"]

    def test_parse_multiple_mandates(self):
        """Test parsing multiple mandates"""
        dsl = """
        mandate M001 {
          type: HARD
          title: "First"
          description: "Test"
        }
        mandate M002 {
          type: HARD
          title: "Second"
          description: "Test"
        }
        """
        mandates = DSLParser.parse_mandates(dsl)

        assert len(mandates) == 2
        assert mandates[0]["id"] == "M001"
        assert mandates[1]["id"] == "M002"

    def test_parse_simple_guideline(self):
        """Test parsing simple guideline"""
        dsl = """
        guideline G01 {
          type: SOFT
          title: "Test Guideline"
          description: "Guidelines..."
          category: general
        }
        """
        guidelines = DSLParser.parse_guidelines(dsl)

        assert len(guidelines) == 1
        assert guidelines[0]["id"] == "G01"
        assert guidelines[0]["type"] == "SOFT"
        assert guidelines[0]["title"] == "Test Guideline"

    def test_parse_guideline_with_examples(self):
        """Test parsing guideline with examples"""
        dsl = """
        guideline G01 {
          type: SOFT
          title: "Test"
          description: "Test"
          examples: ["Example 1", "Example 2"]
        }
        """
        guidelines = DSLParser.parse_guidelines(dsl)

        assert len(guidelines) == 1
        assert guidelines[0]["examples"] == ["Example 1", "Example 2"]

    def test_parse_multiple_guidelines(self):
        """Test parsing multiple guidelines"""
        dsl = """
        guideline G01 {
          type: SOFT
          title: "First"
          description: "Test"
        }
        guideline G02 {
          type: SOFT
          title: "Second"
          description: "Test"
        }
        """
        guidelines = DSLParser.parse_guidelines(dsl)

        assert len(guidelines) == 2
        assert guidelines[0]["id"] == "G01"
        assert guidelines[1]["id"] == "G02"


class TestStringPool:
    """Test string deduplication"""

    def test_string_deduplication(self):
        """Test identical strings get same index"""
        pool = StringPool()

        idx1 = pool.add("Common String")
        idx2 = pool.add("Common String")

        assert idx1 == idx2
        assert len(pool.pool) == 1

    def test_different_strings_different_indices(self):
        """Test different strings get different indices"""
        pool = StringPool()

        idx1 = pool.add("String 1")
        idx2 = pool.add("String 2")

        assert idx1 != idx2
        assert len(pool.pool) == 2

    def test_none_strings_ignored(self):
        """Test None strings don't get added"""
        pool = StringPool()

        idx = pool.add(None)

        assert idx is None
        assert len(pool.pool) == 0

    def test_empty_strings_ignored(self):
        """Test empty strings don't get added"""
        pool = StringPool()

        idx = pool.add("")

        assert idx is None
        assert len(pool.pool) == 0

    def test_pool_array_generation(self):
        """Test pool array generation"""
        pool = StringPool()

        idx1 = pool.add("First")
        idx2 = pool.add("Second")

        pool_array = pool.get_array()

        assert len(pool_array) == 2
        assert pool_array[idx1] == "First"
        assert pool_array[idx2] == "Second"


class TestDSLCompiler:
    """Test DSL compiler"""

    def test_compile_single_mandate(self):
        """Test compiling single mandate"""
        dsl = """
        mandate M001 {
          type: HARD
          title: "Clean Architecture"
          description: "Applications MUST..."
          category: architecture
        }
        """
        compiler = DSLCompiler()
        output = compiler.compile(dsl)

        assert output is not None
        assert len(output["mandates"]) == 1
        assert output["mandates"][0]["id"] == 1

    def test_compile_single_guideline(self):
        """Test compiling single guideline"""
        dsl = """
        guideline G01 {
          type: SOFT
          title: "Test Guideline"
          description: "Guidelines..."
          category: general
        }
        """
        compiler = DSLCompiler()
        output = compiler.compile(dsl)

        assert output is not None
        assert len(output["guidelines"]) == 1
        assert output["guidelines"][0]["id"] == 1

    def test_compile_with_string_deduplication(self):
        """Test string deduplication during compilation"""
        dsl = """
        mandate M001 {
          type: HARD
          title: "Shared Title"
          description: "Shared Title"
          category: general
        }
        """
        compiler = DSLCompiler()
        compiler.compile(dsl)

        # "Shared Title" should only appear once in pool
        assert len(compiler.string_pool.pool) == 1

    def test_compilation_metrics(self):
        """Test compilation metrics"""
        dsl = """
        mandate M001 {
          type: HARD
          title: "Test"
          description: "Test"
          category: general
        }
        """
        compiler = DSLCompiler()
        compiler.compile(dsl)

        metrics = compiler.get_metrics()

        assert metrics.input_size > 0
        assert metrics.output_size > 0
        assert metrics.compilation_time_ms >= 0
        assert metrics.mandates_compiled == 1
        assert metrics.success

    def test_compression_ratio(self):
        """Test compression ratio calculation"""
        metrics = CompilationMetrics(input_size=1000, output_size=400)

        assert metrics.compression_ratio == 0.6  # 60%

    def test_validation_error_handling(self):
        """Test validation errors are caught"""
        dsl = """
        mandate M001 {
          type: HARD
          title: "Test"
        }
        """
        compiler = DSLCompiler()
        output = compiler.compile(dsl, validate=True)

        assert output is None
        assert len(compiler.metrics.errors) > 0


class TestIntegration:
    """Integration tests"""

    def test_compile_mixed_mandates_and_guidelines(self):
        """Test compiling mixed content"""
        dsl = """
        mandate M001 {
          type: HARD
          title: "Mandate One"
          description: "Description one"
          category: architecture
        }
        mandate M002 {
          type: HARD
          title: "Mandate Two"
          description: "Description two"
          category: general
        }
        guideline G01 {
          type: SOFT
          title: "Guideline One"
          description: "Description one"
          category: git
        }
        guideline G02 {
          type: SOFT
          title: "Guideline Two"
          description: "Description two"
          category: general
        }
        """
        output, metrics = compile_string(dsl)

        assert output is not None
        assert len(output["mandates"]) == 2
        assert len(output["guidelines"]) == 2
        assert metrics.mandates_compiled == 2
        assert metrics.guidelines_compiled == 2

    def test_compile_to_file(self):
        """Test compiling to file"""
        dsl = """
        mandate M001 {
          type: HARD
          title: "Test"
          description: "Test"
          category: general
        }
        """

        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = Path(tmpdir) / "test.spec"
            output_file = Path(tmpdir) / "test.compiled.json"

            input_file.write_text(dsl)

            metrics = compile_file(str(input_file), str(output_file))

            assert metrics.success
            assert output_file.exists()

            with open(output_file) as f:
                output = json.load(f)

            assert len(output["mandates"]) == 1

    def test_compile_complex_structure(self):
        """Test compiling complex structure"""
        dsl = """
        mandate M001 {
          type: HARD
          title: "Complex Mandate"
          description: "This is a complex description with multiple sentences and details."
          category: architecture
          rationale: "Because it is important for system design"
          validation: {
            commands: ["pytest", "mypy", "black", "coverage"]
          }
        }
        guideline G01 {
          type: SOFT
          title: "Complex Guideline"
          description: "This is a complex guideline with detailed information."
          category: general
          examples: ["Example 1 with details", "Example 2 with more details", "Example 3"]
        }
        """
        output, metrics = compile_string(dsl)

        assert output is not None
        assert metrics.success
        # Note: Small test cases may have negative compression due to JSON overhead
        # Real data (mandate.spec + guidelines.dsl) will show >65% compression


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
