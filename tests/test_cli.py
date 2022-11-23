"""Tests for `slacktube`.cli module."""
from typing import List

import pytest
from click.testing import CliRunner

import slacktube
from slacktube import cli


@pytest.mark.parametrize(
    "options,expected",
    [
        ([], "slacktube.cli.main"),
        (["--help"], "Usage: main [OPTIONS]"),
        (["--version"], f"main, version { slacktube.__version__ }\n"),
    ],
)
def test_command_line_interface(options: List[str], expected: str) -> None:
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main, options)
    assert result.exit_code == 0
    assert expected in result.output
