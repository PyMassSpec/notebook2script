# stdlib
import pathlib
import re
from textwrap import dedent

# 3rd party
from click.testing import CliRunner, Result
from domdf_python_tools.paths import PathPlus, in_directory

# this package
from notebook2script import convert_notebook, process_multiple_notebooks
from notebook2script.__main__ import main

tests_dir = pathlib.Path(__file__).parent.absolute()


def check_output(outfile: PathPlus):
	# print(outfile)

	assert outfile.is_file()

	expected = []

	for line in dedent(
			"""\
	#!/usr/bin/env python
	# # notebook2script Example Notebook
	# This file exists to test that notebook2script operates correctly
	# ------------------
	# The Jupyter logo should appear below
	# <img width='250px' align='left' src='http://jupyter.org/assets/try/jupyter.png'>
	# In[1]:
	print("hello world")
	# Let's start with some basic numerical operations.
	# In[2]:
	print(1 + 1)
	# In[3]:
	print(2 * 2)
	# In[4]:
	print(4 / 2)
	# In[5]:
	print(3 - 2)
	# In[6]:
	print(2 + 3)
	# In[7]:
	print(2 / 3)
	# In[8]:
	type(3)
	# In[9]:
	type(3.0)
	# In[10]:
	type('3')
	# In[11]:
	print('3' + '3')
	"""
			).split('\n'):
		if not re.match(r"^#*\s*$", line):
			continue
		else:
			expected.append(line)

	actual = []

	for line in outfile.read_text().split('\n'):
		if not re.match(r"^#*\s*$", line):
			continue
		else:
			actual.append(line)

	for e_line, a_line in zip(expected, actual):
		assert e_line == a_line


def test_process_multiple_notebooks(tmp_pathplus):
	notebooks = [tests_dir / "example_notebook.ipynb"]
	outdir = tmp_pathplus / "output"
	assert process_multiple_notebooks(notebooks, outdir) == 0
	check_output(outdir / "example_notebook.py")


def test_convert_notebook(tmp_pathplus):
	notebook = tests_dir / "example_notebook.ipynb"
	outfile = tmp_pathplus / "output" / "example_notebook.py"
	convert_notebook(notebook, outfile)
	check_output(outfile)


def test_cli(tmp_pathplus):
	outdir = tmp_pathplus / "output/"

	with in_directory(tmp_pathplus):
		runner = CliRunner()
		result: Result = runner.invoke(
				main,
				catch_exceptions=False,
				args=[str(tests_dir / "example_notebook.ipynb"), "--outdir", str(outdir)],
				)
		assert result.exit_code == 0
		assert result.stdout == dedent(
				f"""\
			Converting {tests_dir}/example_notebook.ipynb to {tmp_pathplus}/output/example_notebook.py
			"""
				)

	check_output(outdir / "example_notebook.py")


def test_cli_glob(tmp_pathplus):
	outdir = tmp_pathplus / "output/"

	with in_directory(tmp_pathplus):
		runner = CliRunner()
		result: Result = runner.invoke(
				main,
				catch_exceptions=False,
				args=[str(tests_dir / "*.ipynb"), "--outdir", str(outdir)],
				)
		assert result.exit_code == 0
		assert result.stdout == dedent(
				f"""\
			Converting {tests_dir}/example_notebook.ipynb to {tmp_pathplus}/output/example_notebook.py
			"""
				)

	check_output(outdir / "example_notebook.py")
