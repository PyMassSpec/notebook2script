################################################################################
#                                                                              #
#    Copyright (C) 2020 Dominic Davis-Foster                                   #
#                                                                              #
#    This program is free software; you can redistribute it and/or modify      #
#    it under the terms of the GNU General Public License version 2 as         #
#    published by the Free Software Foundation.                                #
#                                                                              #
#    This program is distributed in the hope that it will be useful,           #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#    GNU General Public License for more details.                              #
#                                                                              #
#    You should have received a copy of the GNU General Public License         #
#    along with this program; if not, write to the Free Software               #
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.                 #
#                                                                              #
################################################################################
# stdlib
import argparse
import glob
import os
import pathlib
import sys
import warnings
from pprint import pprint

# this package
from notebook2script.ipynb2py import convert_notebook
from notebook2script.pointless import Pointless

sys.path.append("..")
sys.path.append("../..")

linter = Pointless()


def main():
	# Strip out the current working directory from sys.path.
	# Having the working directory in `sys.path` means that `pylint` might
	# inadvertently import user code from modules having the same name as
	# stdlib or pylint's own modules.
	# CPython issue: https://bugs.python.org/issue33053
	if sys.path[0] == "" or sys.path[0] == os.getcwd():
		sys.path.pop(0)

	parser = argparse.ArgumentParser(description='Convert Jupyter Notebooks to Python scripts')

	parser.add_argument('notebooks', metavar="NOTEBOOK", type=str, nargs='+', help='The notebooks to convert')
	parser.add_argument(
		"-o", '--outdir', type=pathlib.Path, default=pathlib.Path.cwd(),
		help='Directory to save the output scripts in.')  # yapf: disable
	parser.add_argument("-f", '--overwrite', action='store_true', help="Overwrite existing files.")

	args = parser.parse_args()

	notebooks = []

	for notebook in args.notebooks:
		notebooks += glob.glob(notebook)

	# pprint(notebooks)
	# print(notebooks[0])

	if not notebooks:
		parser.error("the following arguments are required: NOTEBOOK")

	process_multiple_notebooks(notebooks, args.outdir, overwrite=args.overwrite)


def process_multiple_notebooks(notebooks, outdir, overwrite=False):
	all_notebooks = []

	for notebook in notebooks:
		all_notebooks += glob.glob(str(notebook))

	print(all_notebooks)
	# input(">")

	for notebook in all_notebooks:
		notebook = pathlib.Path(notebook)
		outfile = outdir / f"{notebook.stem}.py"

		if outfile.is_file() and not overwrite:
			warnings.warn(f"Skipping existing file {outfile}")
		else:
			if notebook.is_file():
				print(f"Converting {notebook} to {outfile}")
				process_notebook(notebook, outfile)
			else:
				print(f"{notebook} not found")


def process_notebook(notebook, outfile):
	convert_notebook(notebook, outfile)
	linter.process_file(outfile)


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.exit(1)
