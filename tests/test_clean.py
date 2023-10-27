from click.testing import CliRunner
from texutil.scripts.txu import clean
import pytest, os, pathlib


@pytest.fixture(autouse=True)
def create_temp_files():
    sample_file_ext = [
        'aux', 'fdb_latexmk', 'fls', 'log', 'out', 'pdf', 'dvi', 'synctex.gz', 'tex', 'txt', 'py'
    ]

    pathlib.Path('tmp/').mkdir()
    for ext in sample_file_ext:
        pathlib.Path(f'tmp/sample_file.{ext}').touch()

class TestClean:
    def test_clean_requires_argument(self):
        runner = CliRunner()
        result = runner.invoke(clean)
        assert result.exit_code == 2