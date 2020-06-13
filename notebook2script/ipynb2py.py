"""
Convert ipynb notebook to python script

Requires nbconvert (pip install nbconvert) and pandoc (apt-get install pandoc)
"""
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

# 3rd party
from nbconvert import PythonExporter  # type: ignore

py_exporter = PythonExporter()


def convert_notebook(nb_file, outfile):
	"""
	Convert a notebook to a python file

	:param nb_file: Filename of the Jupyter Notebook to convert
	:type nb_file: pathlib.Path
	:param outfile: Filename to save the output script as
	:type outfile: pathlib.Path
	"""

	script, *_ = py_exporter.from_file(str(nb_file))

	if not outfile.parent.is_dir():
		outfile.parent.mkdir(parents=True)

	with outfile.open("w") as fp:
		fp.write(script)
