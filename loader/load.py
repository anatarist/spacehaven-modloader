
import os
import shutil
import tempfile

import loader.assets.library
import loader.assets.merge


def load(jarPath, modPaths):
  """Load mods into spacehaven.jar"""

  unload(jarPath)

  coreDirectory = tempfile.TemporaryDirectory()
  corePath = coreDirectory.name

  loader.assets.library.extract(jarPath, corePath)
  loader.assets.merge.mods(corePath, modPaths)

  os.rename(jarPath, jarPath + '.vanilla')
  loader.assets.library.patch(jarPath + '.vanilla', corePath, jarPath)

  coreDirectory.cleanup()


def unload(jarPath):
  """Unload mods from spacehaven.jar"""

  vanillaPath = jarPath + '.vanilla'

  if not os.path.exists(vanillaPath):
    return

  os.remove(jarPath)
  os.rename(vanillaPath, jarPath)
