
import os
import distutils.version

from xml.etree import ElementTree

import version


class ModDatabase:
    """Information about a collection of mods"""

    def __init__(self, path):
        self.path = path
        self.locateMods()

    def locateMods(self):
        self.mods = []

        for modFolder in os.listdir(self.path):
            if modFolder == 'spacehaven':
                continue  # don't need to load core game definitions

            self.mods.append(Mod(os.path.join(self.path, modFolder)))

        self.mods.sort(key=lambda mod: mod.name)


class Mod:
    """Details about a specific mod (name, description)"""

    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(self.path)

        self.loadInfo()

    def loadInfo(self):
        infoFile = os.path.join(self.path, "info")

        if not os.path.exists(infoFile):
            self.name += " [!]"
            self.description = "Error loading mod: no info file present. Please create one."
            return

        try:
            info = ElementTree.parse(infoFile)
            mod = info.getroot()

            self.name = mod.find("name").text
            self.description = mod.find("description").text
            self.minimumLoaderVersion = mod.find("minimumLoaderVersion").text

            if distutils.version.StrictVersion(self.minimumLoaderVersion) > distutils.version.StrictVersion(version.version):
                self.name += " [!]"
                self.description = "Error loading mod: mod loader version {} is required.".format(self.minimumLoaderVersion)

        except AttributeError as ex:
            print(ex)
            self.name += " [!]"
            self.description = "Error loading mod: error parsing info file."
