
import os
import distutils.version

from xml.etree import ElementTree

import version
import ui.log


class ModDatabase:
    """Information about a collection of mods"""

    def __init__(self, path):
        self.path = path
        self.locateMods()

    def locateMods(self):
        self.mods = []

        ui.log.log("Locating mods...")
        for modFolder in os.listdir(self.path):
            if modFolder == 'spacehaven':
                continue  # don't need to load core game definitions

            if os.path.isfile(modFolder):
                continue  # don't load logs, prefs, etc

            self.mods.append(Mod(os.path.join(self.path, modFolder)))

        self.mods.sort(key=lambda mod: mod.name)


class Mod:
    """Details about a specific mod (name, description)"""

    def __init__(self, path):
        ui.log.log("  Loading mod at {}...".format(path))
        self.path = path
        self.name = os.path.basename(self.path)

        self.loadInfo()

    def loadInfo(self):
        infoFile = os.path.join(self.path, "info")

        if not os.path.exists(infoFile):
            ui.log.log("    No info file present")
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
                ui.log.log("    Minimum loader version is too low")
                self.name += " [!]"
                self.description = "Error loading mod: mod loader version {} is required.".format(self.minimumLoaderVersion)

        except AttributeError as ex:
            print(ex)
            self.name += " [!]"
            self.description = "Error loading mod: error parsing info file."
            ui.log.log("    Failed to parse info file")

        ui.log.log("    Successfully detected {} (minimumLoaderVersion={})".format(self.name, self.minimumLoaderVersion))
