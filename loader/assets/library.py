
import os
import shutil
import click

from zipfile import ZipFile

PATCHABLE_FILES = [
  'library/haven',
  'library/texts',
  'library/animations'
]

def extract(jarPath, corePath):
  if not os.path.exists(corePath):
    os.mkdir(corePath)

  with ZipFile(jarPath, "r") as spacehaven:
    for file in set(spacehaven.namelist()):
      if file.startswith("library/") and not file.endswith("/"):
        spacehaven.extract(file, corePath)


def patch(jarPath, corePath, resultPath):
  original = ZipFile(jarPath, "r")
  patched = ZipFile(resultPath, "w")

  for file in set(original.namelist()):
    if not file.endswith("/") and not file in PATCHABLE_FILES:
      patched.writestr(file, original.read(file))

  for file in PATCHABLE_FILES:
    patched.write(os.path.join(corePath, file.replace('/', os.sep)), file)

  patched.close()
