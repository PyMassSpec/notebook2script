# stdlib
import os

# 3rd party
from coincidence.regressions import AdvancedFileRegressionFixture

# this package
from notebook2script.pointless import Pointless


def test_pointless_checker(tmp_path, advanced_file_regression: AdvancedFileRegressionFixture):
	# Make a file with some "pointless" statements

	outfile = tmp_path / "test_script.py"

	outfile.write_text(
			"""\
#!/use/bin/python3

# Based on https://realpython.com/how-to-use-numpy-arange/

import numpy as np

np.arange(start=1, stop=10, step=3)

np.arange(start=1, stop=10)

np.arange(
	start=1,
	stop=10,
	step=1
	)

np.arange(
	start=1, stop=10, step=1
	)

data = np.arange(10)
data

"""
			)

	linter = Pointless()

	linter.process_file(os.fspath(outfile))

	advanced_file_regression.check_file(outfile)
