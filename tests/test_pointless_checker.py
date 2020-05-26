import tempfile
import pathlib
from notebook2script.pointless import Pointless


def test_pointless_checker():

	with tempfile.TemporaryDirectory() as tmpdir:
		tmpdir = pathlib.Path(tmpdir)

		# Make a file with some "pointless" statements

		outfile = tmpdir / "test_script.py"

		outfile.write_text("""\
#!/use/bin/python3

# Based on https://realpython.com/how-to-use-numpy-arange/

import numpy as np

np.arange(start=1, stop=10, step=3)

np.arange(start=1, stop=10)

np.arange(
	start=1, 
	stop=10, 
	step=1,
	)

np.arange(
	start=1, stop=10, step=1
	)
	
data = np.arange(10)
data

""")

		linter = Pointless()

		linter.process_file(outfile)

		assert outfile.read_text() == """\
#!/use/bin/python3

# Based on https://realpython.com/how-to-use-numpy-arange/

import numpy as np

np.arange(start=1, stop=10, step=3)

np.arange(start=1, stop=10)

np.arange(
	start=1, 
	stop=10, 
	step=1,
	)

np.arange(
	start=1, stop=10, step=1
	)
	
data = np.arange(10)
print(data)
"""
