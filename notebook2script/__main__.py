import os
import sys

sys.path.append("..")
sys.path.append("../..")
print(sys.path)

from pointless import main

# Strip out the current working directory from sys.path.
# Having the working directory in `sys.path` means that `pylint` might
# inadvertently import user code from modules having the same name as
# stdlib or pylint's own modules.
# CPython issue: https://bugs.python.org/issue33053
if sys.path[0] == "" or sys.path[0] == os.getcwd():
	sys.path.pop(0)

try:
	main()
except KeyboardInterrupt:
	sys.exit(1)
