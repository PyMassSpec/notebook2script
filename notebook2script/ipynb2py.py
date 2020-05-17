"""
Convert ipynb notebook to python script

Requires nbconvert (pip install nbcovnert) and pandoc (apt-get install pandoc)
"""

# Import the Python exporter and instantiate it
from nbconvert import PythonExporter
py_exporter = PythonExporter()

from notebook2script import notebooks_dir, scripts_dir
from notebook2script.conf import notebooks


for notebook in notebooks:
	# Convert the notebook to a python file
	script, *_ = py_exporter.from_file(str(notebooks_dir / f"{notebook}.ipynb"))
	
	with open(scripts_dir / f"{notebook}.py", "w") as fp:
		fp.write(script)
