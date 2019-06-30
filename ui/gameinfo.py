
import hashlib

import ui.log

KNOWN_VERSIONS = {
    '11a3cc26d5afe56906cd5831627c303878074dac3788f623eca7d340c9e30ad3': '0.4.1', # MacOS
    'dbd84fa985de37f806f40bf6035f0603be9ee66b0df67a9612a182469a7531e2': '0.4.1'  # Windows
}


class GameInfo:
    def __init__(self, jarPath):
        self.jarPath = jarPath

        self.detectVersion()

    def detectVersion(self):
        ui.log.log("Loading game information...")

        hasher = hashlib.sha256()
        with open(self.jarPath, 'rb') as f:
            hasher.update(f.read())

        hash = hasher.hexdigest()

        if hash in KNOWN_VERSIONS:
            self.version = KNOWN_VERSIONS[hash]
        else:
            self.version = None

        ui.log.log("  Version: {} (hash {})".format(self.version, hash))
