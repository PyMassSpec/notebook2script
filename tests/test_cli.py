import pathlib

from notebook2script.__main__ import process_multiple_notebooks

tests_dir = pathlib.Path(__file__).parent.absolute()


def test_cli_backend():
	notebooks = [tests_dir / "*.ipynb"]
	outdir = tests_dir / "output/"
	process_multiple_notebooks(notebooks, outdir)

	outfile = outdir / "example_notebook.py"
	print(outfile)
	assert outfile.is_file()

	assert outfile.read_text() == """\
#!/usr/bin/env python
# coding: utf-8

# # notebook2script Example Notebook

# This file exists to test that notebook2script operates correctly

# ------------------

# The Jupyter logo should appear below
# 
# <img width='250px' align='left' src='http://jupyter.org/assets/try/jupyter.png'>
# 

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

	outfile.unlink()
	outdir.rmdir()
