
import os
import shutil
import tempfile

import loader.assets.library
import loader.assets.merge

import ui.log


def load(jarPath, modPaths):
    """Load mods into spacehaven.jar"""

    unload(jarPath)

    coreDirectory = tempfile.TemporaryDirectory()
    corePath = coreDirectory.name

    ui.log.log("Loading mods...")
    ui.log.log("  jarPath: {}".format(jarPath))
    ui.log.log("  corePath: {}".format(corePath))
    ui.log.log("  modPaths:\n  {}".format("\n  ".join(modPaths)))

    loader.assets.library.extract(jarPath, corePath)
    loader.assets.merge.mods(corePath, modPaths)

    os.rename(jarPath, jarPath + '.vanilla')
    loader.assets.library.patch(jarPath + '.vanilla', corePath, jarPath)

    coreDirectory.cleanup()


def unload(jarPath):
    """Unload mods from spacehaven.jar"""

    vanillaPath = jarPath + '.vanilla'

    ui.log.log("Unloading mods...")
    if not os.path.exists(vanillaPath):
        ui.log.log("  No active mods")
        return

    ui.log.log("  Unloading {} from {}".format(jarPath, vanillaPath))
    os.remove(jarPath)
    os.rename(vanillaPath, jarPath)
