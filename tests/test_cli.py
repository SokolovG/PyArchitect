from pathlib import Path

from click.testing import CliRunner

from src.main import cli


class TestCli:

    def test_init_command(self) -> None:
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ["init", "--preset", "standard"])
            assert result.exit_code == 0
            assert "Generated standard config" in result.output
            assert Path("ddd-config.yaml").exists()

    def test_init_command_with_existing_file(self) -> None:
        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("ddd-config.yaml").touch()

            result = runner.invoke(cli, ["init", "--preset", "standard"])
            assert result.exit_code == 0
            assert "Config file already exists" in result.output

    def test_init_command_with_force_flag(self) -> None:
        runner = CliRunner()
        with runner.isolated_filesystem():
            Path("ddd-config.yaml").write_text("old content")

            result = runner.invoke(cli, ["init", "--preset", "standard", "--force"])
            assert result.exit_code == 0
            assert "Overwriting existing config file" in result.output
            assert Path("ddd-config.yaml").exists()

    def test_init_command_with_invalid_preset(self) -> None:
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ["init", "--preset", "nonexistent"])
            assert result.exit_code == 0
            assert "Unknown preset: nonexistent" in result.output
            assert not Path("ddd-config.yaml").exists()

    def test_validate_command(self) -> None:
        runner = CliRunner()
        with runner.isolated_filesystem():
            runner.invoke(cli, ["init", "--preset", "standard"])
            result = runner.invoke(cli, ["validate"])
            assert "Configuration validated successfully" in result.output
            assert result.exit_code == 0

    def test_validate_command_with_file_parameter(self) -> None:
        runner = CliRunner()
        with runner.isolated_filesystem():
            runner.invoke(cli, ["init", "--preset", "standard"])
            result = runner.invoke(cli, ["validate", "--file", "ddd-config.yaml"])
            assert "Configuration validated successfully" in result.output
            assert result.exit_code == 0

    def test_validate_command_with_missing_file(self) -> None:
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ["validate"])
            assert "Configuration file not found" in result.output

    def test_run_command(self) -> None:
        runner = CliRunner()
        with runner.isolated_filesystem():
            runner.invoke(cli, ["init", "--preset", "standard"])
            result = runner.invoke(cli, ["run"])
            assert result.exit_code == 0
            assert "Project generation completed successfully" in result.output

    def test_run_command_with_file_parameter(self) -> None:
        runner = CliRunner()
        with runner.isolated_filesystem():
            runner.invoke(cli, ["init", "--preset", "standard"])
            result = runner.invoke(cli, ["run", "--file", "ddd-config.yaml"])
            assert result.exit_code == 0
            assert "Project generation completed successfully" in result.output

    def test_run_command_with_missing_file(self) -> None:
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ["run", "--file", "nonexistent.yaml"])
            assert result.exit_code == 0
            assert "Config file not found" in result.output

    def test_preview_command(self) -> None:
        runner = CliRunner()
        with runner.isolated_filesystem():
            runner.invoke(cli, ["init", "--preset", "standard"])
            result = runner.invoke(cli, ["preview"])
            assert result.exit_code == 0
            assert "Project generation started" in result.output

    def test_preview_command_with_file_parameter(self) -> None:
        runner = CliRunner()
        with runner.isolated_filesystem():
            runner.invoke(cli, ["init", "--preset", "standard"])
            result = runner.invoke(cli, ["preview", "--file", "ddd-config.yaml"])
            assert result.exit_code == 0
            assert "Project generation started" in result.output

    def test_preview_command_with_missing_file(self) -> None:
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ["preview", "--file", "nonexistent.yaml"])
            assert result.exit_code == 0
            assert "Config file not found" in result.output

    def test_command_arguments(self) -> None:
        """Test commands with invalid arguments"""
        runner = CliRunner()

        result = runner.invoke(cli, ["nonexistent"])
        assert result.exit_code != 0
        assert "No such command" in result.output

        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "PyArch command-line tool" in result.output

        result = runner.invoke(cli, ["init", "--help"])
        assert result.exit_code == 0
        assert "Generate basic example configuration" in result.output

    def test_beauty_errors(self) -> None:
        """Test error handling and user-friendly error messages"""
        runner = CliRunner()

        with runner.isolated_filesystem():
            Path("invalid.yaml").write_text("invalid: yaml: content: [")

            result = runner.invoke(cli, ["validate", "--file", "invalid.yaml"])
            assert result.exit_code == 0
            assert "Configuration file could not be parsed" in result.output

            result = runner.invoke(cli, ["run", "--file", "invalid.yaml"])
            assert result.exit_code == 0
            assert (
                "Configuration file could not be parsed" in result.output
                or "Error" in result.output
            )

    def test_cli_group_functionality(self) -> None:
        """Test the main CLI group"""
        runner = CliRunner()

        result = runner.invoke(cli, [])
        assert result.exit_code == 2

        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "init" in result.output
        assert "validate" in result.output
        assert "run" in result.output
        assert "preview" in result.output
