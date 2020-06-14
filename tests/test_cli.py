# stdlib
import pathlib
import re

# this package
from notebook2script.__main__ import process_multiple_notebooks

tests_dir = pathlib.Path(__file__).parent.absolute()


def test_cli_backend():
	notebooks = [tests_dir / "*.ipynb"]
	outdir = tests_dir / "output/"
	process_multiple_notebooks(notebooks, outdir)

	outfile = outdir / "example_notebook.py"
	print(outfile)
	assert outfile.is_file()

	expected = []

	for line in """\
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
""".split("\n"):
		if not re.match(r"^#*\s*$", line):
			continue
		else:
			expected.append(line)

	actual = []

	for line in outfile.read_text().split("\n"):
		if not re.match(r"^#*\s*$", line):
			continue
		else:
			actual.append(line)

	for e_line, a_line in zip(expected, actual):
		assert e_line == a_line

	outfile.unlink()
	outdir.rmdir()
