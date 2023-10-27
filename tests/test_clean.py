from click.testing import CliRunner
from texutil.scripts.txu import clean
import pytest, os, pathlib, shutil


@pytest.fixture(autouse=True)
def create_temp_files():
    sample_file_ext = [
        'aux', 'fdb_latexmk', 'fls', 'log', 'out', 'pdf', 'dvi', 'synctex.gz', 'tex', 'txt', 'py'
    ]

    pathlib.Path('tmp/').mkdir(exist_ok=True)
    for ext in sample_file_ext:
        pathlib.Path(f'tmp/sample_file.{ext}').touch()

    yield # wait until after test execution

    shutil.rmtree('tmp/')

class TestClean:
    def test_clean_requires_argument(self):
        runner = CliRunner()
        result = runner.invoke(clean)
        assert result.exit_code == 2
    
    def test_clean_verifies_directory(self):
        runner = CliRunner()
        result = runner.invoke(clean, ['bad_dir'])
        assert result.exit_code == 2
    
    def test_clean_removes_trailing_slash(self):
        runner = CliRunner()
        result = runner.invoke(clean, ['tmp/'])
        assert result.exit_code == 0

    def test_clean_ignores_one_option(self):
        runner = CliRunner()
        result = runner.invoke(clean, ['-i', 'pdf', 'tmp/'])
        assert result.exit_code == 0
        assert os.path.exists('tmp/sample_file.pdf') == True

    def test_clean_ignores_two_options(self):
        runner = CliRunner()
        result = runner.invoke(clean, ['-i', 'pdf', '-i', 'log', 'tmp/'])
        assert result.exit_code == 0
        assert os.path.exists('tmp/sample_file.pdf') == True
        assert os.path.exists('tmp/sample_file.log') == True
    
    def test_clean_ignores_tex(self):
        runner = CliRunner()
        result = runner.invoke(clean, ['tmp/'])
        assert result.exit_code == 0
        assert os.path.exists('tmp/sample_file.tex') == True

    def test_clean_ignores_non_tex_file(self):
        runner = CliRunner()
        result = runner.invoke(clean, ['tmp/'])
        assert result.exit_code == 0
        assert os.path.exists('tmp/sample_file.txt') == True
        assert os.path.exists('tmp/sample_file.py') == True