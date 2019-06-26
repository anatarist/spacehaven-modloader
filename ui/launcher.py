
def launch(path):
  if path is None:
    return

  if sys.platform == 'win32':
    os.startfile(path)
  elif sys.platform == 'darwin':
    subprocess.call(["open", path])
  else:
    subprocess.call(["xdg-open", path])
