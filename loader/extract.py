
import loader.assets.library
import loader.assets.explode
import loader.assets.annotate

def extract(jarPath, modPath):
  """Extract and annotate game assets"""

  loader.assets.library.extract(jarPath, modPath)

  # loader.assets.explode.explode()
  # loader.assets.annotate.annotate()
