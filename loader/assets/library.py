
import os
import shutil
import click

from zipfile import ZipFile


def extract(jarPath, modPath):
  coreDefsPath = os.path.join(modPath, "spacehaven")

  if not os.path.exists(coreDefsPath):
    os.mkdir(coreDefsPath)

  with ZipFile(jarPath, "r") as spacehaven:
    for file in set(spacehaven.namelist()):
      if file.startswith("library/") and not file.endswith("/"):
        spacehaven.extract(file, coreDefsPath)


def patch(files):
  original = ZipFile(spacehaven_jar, "r")
  patched = ZipFile(spacehaven_jar + ".patched", "w")

  for file in set(original.namelist()):
    if not file.endswith("/") and not file in files:
      patched.writestr(file, original.read(file))

  for file in files:
    patched.write("spacehaven/{}".format(file), file)

  patched.close()

  shutil.copy(
    spacehaven_jar,
    spacehaven_jar + ".1"
  )

  shutil.move(
    spacehaven_jar + ".patched",
    spacehaven_jar
  )

  print("Patched Space Haven: {} files".format(len(files)))
