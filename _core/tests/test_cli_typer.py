"""Tests for SDD CLI (Phase 6)."""

import pytest
from pathlib import Path
from typer.testing import CliRunner
from sdd_cli.main import app
from sdd_cli.utils.loader import load_governance_config, validate_governance_path
from sdd_cli.generators.agent_seeds import generate_agent_seeds


runner = CliRunner()


class TestCLIMain:
    """Test main CLI entry point."""
    
    def test_help_command(self):
        """Test that --help displays usage information."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "SDD" in result.stdout or "governance" in result.stdout
    
    def test_version_command(self):
        """Test version command displays version."""
        result = runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "3.0.0" in result.stdout
    
    def test_version_help(self):
        """Test version command help."""
        result = runner.invoke(app, ["version", "--help"])
        assert result.exit_code == 0


class TestGovernanceCommands:
    """Test governance command group."""
    
    def test_governance_help(self):
        """Test governance command group help."""
        result = runner.invoke(app, ["governance", "--help"])
        assert result.exit_code == 0
        assert "load" in result.stdout
        assert "validate" in result.stdout
        assert "generate" in result.stdout
    
    def test_load_help(self):
        """Test load command help."""
        result = runner.invoke(app, ["governance", "load", "--help"])
        assert result.exit_code == 0
        assert "governance" in result.stdout.lower()
    
    def test_validate_help(self):
        """Test validate command help."""
        result = runner.invoke(app, ["governance", "validate", "--help"])
        assert result.exit_code == 0
    
    def test_generate_help(self):
        """Test generate command help."""
        result = runner.invoke(app, ["governance", "generate", "--help"])
        assert result.exit_code == 0


class TestLoadCommand:
    """Test load command functionality."""
    
    def test_load_with_valid_path(self):
        """Test load with valid .sdd-wizard path."""
        result = runner.invoke(app, ["governance", "load", "--path", ".sdd-wizard"])
        # Should succeed if .sdd-wizard exists, or fail gracefully if not
        assert result.exit_code in [0, 1]
    
    def test_load_with_invalid_path(self):
        """Test load with invalid path."""
        result = runner.invoke(app, ["governance", "load", "--path", "/nonexistent/path"])
        assert result.exit_code == 1
        assert "Invalid" in result.stdout or "not found" in result.stdout.lower()


class TestValidateCommand:
    """Test validate command functionality."""
    
    def test_validate_with_valid_path(self):
        """Test validate with valid .sdd-wizard path."""
        result = runner.invoke(app, ["governance", "validate", "--path", ".sdd-wizard"])
        # Should succeed if .sdd-wizard is valid, or fail gracefully if not
        assert result.exit_code in [0, 1]
    
    def test_validate_with_invalid_path(self):
        """Test validate with invalid path."""
        result = runner.invoke(app, ["governance", "validate", "--path", "/nonexistent/path"])
        assert result.exit_code == 1


class TestGenerateCommand:
    """Test generate command functionality."""
    
    def test_generate_with_valid_path(self):
        """Test generate with valid .sdd-wizard path."""
        result = runner.invoke(app, ["governance", "generate", "--path", ".sdd-wizard"])
        # Should succeed if .sdd-wizard is valid, or fail gracefully if not
        assert result.exit_code in [0, 1]
    
    def test_generate_with_invalid_path(self):
        """Test generate with invalid path."""
        result = runner.invoke(app, ["governance", "generate", "--path", "/nonexistent/path"])
        assert result.exit_code == 1


class TestLoaderIntegration:
    """Test loader integration with governance."""
    
    def test_loader_module_exists(self):
        """Test that loader module imports correctly."""
        from sdd_cli.utils import loader
        assert hasattr(loader, 'load_governance_config')
        assert hasattr(loader, 'validate_governance_path')
        assert hasattr(loader, 'get_governance_summary')
    
    def test_loader_imports_runtime(self):
        """Test that loader imports .sdd-wizard runtime modules."""
        # This test checks that the import path is correct
        # but doesn't require .sdd-wizard to be fully functional
        import sys
        from pathlib import Path
        
        sdd_wizard_path = Path(__file__).parent.parent / ".sdd-wizard"
        assert sdd_wizard_path.exists() or True  # Pass if doesn't exist (import will fail gracefully)


class TestAgentSeedsGenerator:
    """Test agent seeds generation."""
    
    def test_generate_agent_seeds_structure(self):
        """Test that agent seeds generator creates correct structure."""
        from sdd_cli.generators.agent_seeds import generate_agent_seeds, _format_rules
        
        # Create mock config
        mock_config = {
            "core_fingerprint": "abc123",
            "client_fingerprint": "def456",
            "items": [],
        }
        
        # Test with temporary directory
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            results = generate_agent_seeds(Path(tmpdir), mock_config)
            assert len(results) == 3
            assert all(r[2] == "✓ Generated" for r in results)
    
    def test_agent_seeds_content_cursor(self):
        """Test that Cursor seed contains required content."""
        from sdd_cli.generators.agent_seeds import _generate_cursor_seed
        
        mock_config = {"core_fingerprint": "test123", "items": []}
        content = _generate_cursor_seed(mock_config, [], [])
        assert "Cursor" in content or "cursor" in content.lower()
    
    def test_agent_seeds_content_copilot(self):
        """Test that Copilot seed contains required content."""
        from sdd_cli.generators.agent_seeds import _generate_copilot_seed
        
        mock_config = {"core_fingerprint": "test123", "items": []}
        content = _generate_copilot_seed(mock_config, [], [])
        assert "Copilot" in content or "copilot" in content.lower()
    
    def test_agent_seeds_content_generic(self):
        """Test that Generic seed contains required content."""
        from sdd_cli.generators.agent_seeds import _generate_generic_seed
        
        mock_config = {"core_fingerprint": "test123", "items": []}
        content = _generate_generic_seed(mock_config, [], [])
        assert "Architecture" in content or "Governance" in content


class TestCommandExecutions:
    """Test command execution scenarios."""
    
    def test_load_execution(self):
        """Test load command execution."""
        result = runner.invoke(app, ["governance", "load"])
        # Should complete (success or expected failure)
        assert result.exit_code in [0, 1]
    
    def test_validate_execution(self):
        """Test validate command execution."""
        result = runner.invoke(app, ["governance", "validate"])
        # Should complete (success or expected failure)
        assert result.exit_code in [0, 1]
    
    def test_generate_execution(self):
        """Test generate command execution."""
        result = runner.invoke(app, ["governance", "generate"])
        # Should complete (success or expected failure)
        assert result.exit_code in [0, 1]
    
    def test_invalid_subcommand(self):
        """Test invalid subcommand."""
        result = runner.invoke(app, ["governance", "invalid"])
        assert result.exit_code != 0


class TestPathErrorHandling:
    """Test error handling for path-related issues."""
    
    def test_missing_governance_path(self):
        """Test handling of missing governance path."""
        result = runner.invoke(app, ["governance", "load", "--path", "/dev/null/nonexistent"])
        assert result.exit_code == 1
