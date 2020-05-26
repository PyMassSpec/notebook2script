"""
Convert ipynb notebook to python script

Requires nbconvert (pip install nbconvert) and pandoc (apt-get install pandoc)
"""

from nbconvert import PythonExporter


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

