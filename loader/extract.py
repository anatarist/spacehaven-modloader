
import os

import loader.assets.library
import loader.assets.explode
import loader.assets.annotate


def extract(jarPath, modPath):
  """Extract and annotate game assets"""

  corePath = os.path.join(modPath, "spacehaven")

  loader.assets.library.extract(jarPath, corePath)

  loader.assets.explode.explode(corePath)
  loader.assets.annotate.annotate(corePath)
