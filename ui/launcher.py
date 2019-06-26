
import sys
import subprocess


def launch(path):
  """Open a path in an OS-native way"""

  if path is None:
    return

  if sys.platform == 'win32':
    os.startfile(path)
  elif sys.platform == 'darwin':
    subprocess.call(["open", path])
  else:
    subprocess.call(["xdg-open", path])
