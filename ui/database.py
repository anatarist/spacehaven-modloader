
import os
import distutils.version

from xml.etree import ElementTree

import version
import ui.log
import ui.gameinfo


class ModDatabase:
    """Information about a collection of mods"""

    def __init__(self, path, gameInfo):
        self.path = path
        self.gameInfo = gameInfo
        self.locateMods()

    def locateMods(self):
        self.mods = []

        ui.log.log("Locating mods...")
        for modFolder in os.listdir(self.path):
            if modFolder == 'spacehaven':
                continue  # don't need to load core game definitions

            if os.path.isfile(modFolder):
                continue  # don't load logs, prefs, etc

            self.mods.append(Mod(os.path.join(self.path, modFolder), self.gameInfo))

        self.mods.sort(key=lambda mod: mod.name)


class Mod:
    """Details about a specific mod (name, description)"""

    def __init__(self, path, gameInfo):
        ui.log.log("  Loading mod at {}...".format(path))

        self.path = path
        self.name = os.path.basename(self.path)

        self.gameInfo = gameInfo

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

            self.name = mod.find("name").text.strip()
            self.description = mod.find("description").text.strip() + "\n\n"

            self.verifyLoaderVersion(mod)
            self.verifyGameVersion(mod, self.gameInfo)

        except AttributeError as ex:
            print(ex)
            self.name += " [!]"
            self.description = "Error loading mod: error parsing info file."
            ui.log.log("    Failed to parse info file")

        ui.log.log("    Finished loading {}".format(self.name))

    def verifyLoaderVersion(self, mod):
        self.minimumLoaderVersion = mod.find("minimumLoaderVersion").text
        if distutils.version.StrictVersion(self.minimumLoaderVersion) > distutils.version.StrictVersion(version.version):
            self.warn("Mod loader version {} is required".format(self.minimumLoaderVersion))

        ui.log.log("    Minimum Loader Version: {}".format(self.minimumLoaderVersion))

    def verifyGameVersion(self, mod, gameInfo):
        self.gameVersions = []

        gameVersionsTag = mod.find("gameVersions")
        if gameVersionsTag is None:
            self.warn("This mod does not declare what game version(s) it supports.")
            return

        for version in list(gameVersionsTag):
            self.gameVersions.append(version.text)

        ui.log.log("    Game Versions: {}".format(", ".join(self.gameVersions)))

        if not gameInfo.version:
            self.warn("Could not determine Space Haven version. You might need to update your loader.")
            return

        if not gameInfo.version in self.gameVersions:
            self.warn("This mod may not support Space Haven {}, it only supports {}.".format(
                self.gameInfo.version,
                ", ".join(self.gameVersions)
            ))



    def warn(self, message):
        ui.log.log("    Warning: {}".format(message))
        self.name += " [!]"
        self.description += "\nWarning: {}".format(message)
