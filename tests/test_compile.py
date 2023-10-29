from click.testing import CliRunner
from texutil.scripts.txu import compile
import pytest, os, pathlib, shutil, re, time


@pytest.fixture(autouse=True)
def create_temp_files():

    pathlib.Path('tmp/').mkdir(exist_ok=True)
    with open('tmp/valid.tex', 'w+') as f:
        f.write(r"""
\documentclass{article}

\title{Simple Sample}
\author{My Name}
\date{\today}
\begin{document}
    \maketitle
    
    \section{Hello World!}
    \textbf{Hello World!} Sample \LaTeX.

\end{document}
                """)
        
    with open('tmp/invalid.tex', 'w+') as f:
        f.write(r"""
\documentclass{article}

\title{Simple Sample}
author{My Name}
\date{\today}
\begin{document}
    \mle
    
    \section{Hello World!}
    \textbf{Hello World!} Sample \LaTeX.

\end{document}
                """)
        
    os.chdir('tmp/')

    yield # wait until after test execution

    os.chdir('..')
    shutil.rmtree('tmp/')

class TestCompile:
    def test_compile_requires_argument(self):
        runner = CliRunner()
        result = runner.invoke(compile)
        assert result.exit_code == 2

    def test_compile_fails_with_invalid_tex(self):
        runner = CliRunner()
        result = runner.invoke(compile, ['invalid.tex'])
        assert result.exit_code == 0
        assert 'failed' in result.stdout

    def test_compile_succeeds_with_valid_tex(self):
        runner = CliRunner()
        result = runner.invoke(compile, ['valid.tex'])
        assert result.exit_code == 0
        assert 'Successfully' in result.stdout
        assert os.path.exists('valid.pdf')

    def test_compile_timestamp_works_with_valid_tex(self):
        runner = CliRunner()
        result = runner.invoke(compile, ['--timestamp', 'valid.tex'])
        ls_dir = os.listdir()
        normal_pdf_flag = False
        timestamped_pdf_flag = False

        for file_name in ls_dir:
            if 'valid.pdf' in file_name:
                normal_pdf_flag = True
            if re.search('valid_[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{6}.pdf', file_name):
                timestamped_pdf_flag = True
        
        assert result.exit_code == 0
        assert 'Successfully' in result.stdout
        assert timestamped_pdf_flag
        assert normal_pdf_flag == False

    def test_compile_timestamp_works_with_invalid_tex(self):
        runner = CliRunner()
        result = runner.invoke(compile, ['--timestamp', 'invalid.tex'])
        ls_dir = os.listdir()
        normal_pdf_flag = False
        timestamped_pdf_flag = False

        for file_name in ls_dir:
            if 'valid.pdf' in file_name:
                normal_pdf_flag = True
            if re.search('invalid_[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{6}.pdf', file_name):
                timestamped_pdf_flag = True
        
        assert result.exit_code == 0
        assert 'failed' in result.stdout
        assert timestamped_pdf_flag
        assert normal_pdf_flag == False
