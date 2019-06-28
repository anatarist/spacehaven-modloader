
import os
import sys

import version

class Logger:
    """Logger that writes to both a local logfile and one in the game mods/ folder"""
    def __init__(self):
        self.gameLog = None

        self.localPath = os.path.join(os.path.dirname(sys.argv[0]), "logs.txt")
        self.localLog = open(self.localPath, "w")
        print("Started logging to {}...".format(self.localPath))

        self.logInitialInfo()

    def setGameModPath(self, path):
        self.gameLog = open(os.path.join(path, "logs.txt"), "w")

        self.logInitialInfo()
        self.log("Logging to {}".format(path))

    def logInitialInfo(self):
        self.log("Space Haven Modloader v{}".format(version.version))

    def log(self, message=""):
        print("[LOG] {}".format(message))
        self.localLog.write(message + "\n")

        if self.gameLog:
            self.gameLog.write(message + "\n")


logger = Logger()
log = logger.log
setGameModPath = logger.setGameModPath