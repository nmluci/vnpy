from __future__ import annotations
from typing import List
from dataclasses import dataclass
import json, signal

from utils import NatsumeUtils, NatsumeLogger, Socket

class VNDB:
    def __init__(self):
        self.log = NatsumeLogger("VNDB")
        self.name = "Natsume x VNDB"
        self.utils = NatsumeUtils()

        # Connect to VNDB API
        self.socket = Socket()
        self.socket.connect()
        self.socket.login()

        signal.signal(signal.SIGINT, self.graceExit)
        signal.signal(signal.SIGTERM, self.graceExit)

    def getWebStats(self):
        stats = json.loads(self.socket.communicate("dbstats").decode().split(" ")[1])
        self.utils.printInfo("{:<10}: {}".format("VN", stats["vn"]))
        self.utils.printInfo("{:<10}: {}".format("Producers", stats["producers"]))
        self.utils.printInfo("{:<10}: {}".format("Traits", stats["traits"]))
        self.utils.printInfo("{:<10}: {}".format("Releases", stats["releases"]))
        self.utils.printInfo("{:<10}: {}".format("Staff", stats["staff"]))
        self.utils.printInfo("{:<10}: {}".format("Chars", stats["chars"]))
        self.utils.printInfo("{:<10}: {}".format("Tags", stats["tags"]))
    

    # Format: get type flags filters options
    def get(self, type: str, flags: List[str], filters: List[str], options=None):
        response = self.socket.communicate(r"get {} {} ({})".format(
            type, ",".join(flags), ",".join(filters)))
        return json.loads(response.decode().split("results")[1])

    def graceExit(self, signum=None, frame=None):
        self.socket.disconnect()
        exit()

# driver testdrive
try:
    vndb = VNDB()
    vndb.getWebStats()
    # print(json.dumps(vndb.get("vn", ["basic"], ['search ~ "nekopara"']), indent=3))
    print(json.dumps(vndb.get("vn", ["basic", "details", "tags"], ['title = "Neko Para Vol.2 Shimai Neko no Sucre"']), indent=3))

finally:
    vndb.graceExit()