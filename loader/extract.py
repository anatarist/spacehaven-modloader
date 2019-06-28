
import os

import loader.assets.library
import loader.assets.explode
import loader.assets.annotate

import ui.log

def extract(jarPath, corePath):
    """Extract and annotate game assets"""

    ui.log.log("Running extract & annotate")

    loader.assets.library.extract(jarPath, corePath)

    loader.assets.explode.explode(corePath)
    loader.assets.annotate.annotate(corePath)
