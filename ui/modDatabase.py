
import os

from xml.etree import ElementTree

class Mod:
  def __init__(self, path):
    self.path = path
    self.name = os.path.basename(self.path)

    self.loadInfo()

  def loadInfo(self):
    infoFile = os.path.join(self.path, "info")

    if not os.path.exists(infoFile):
      self.description = "Cannot load mod: no info file present. Please create one."
      return

    try:
      info = ElementTree.parse(infoFile)
      mod = info.getroot()

      self.name = mod.find("name").text
      self.description = mod.find("description").text

    except AttributeError as ex:
      print(ex)
      self.description = "Cannot load mod: error parsing info file."

class ModDatabase:
  def __init__(self, path):
    self.path = path
    self.locateMods()

  def locateMods(self):
    self.mods = []

    for modFolder in os.listdir(self.path):
      if modFolder == 'spacehaven':
        continue # don't need to load core game definitions

      self.mods.append(Mod(os.path.join(self.path, modFolder)))

    self.mods.sort(key=lambda mod: mod.name)
