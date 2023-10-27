from click.testing import CliRunner
from texutil.scripts.txu import clean
import pytest

def test_clean_requires_argument():
    runner = CliRunner()
    result = runner.invoke(clean)
    assert result.exit_code == 2

