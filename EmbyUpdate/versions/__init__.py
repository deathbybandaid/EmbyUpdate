import os
import sys
import platform

from EmbyUpdate import EmbyUpdate_VERSION
from EmbyUpdate.tools import is_docker


class Versions():
    """
    EmbyUpdate versioning management system.
    """

    def __init__(self, settings, logger, web):
        self.logger = logger
        self.web = web

        self.dict = {}

        self.register_EmbyUpdate()

        self.register_env()

        self.get_online_versions()

        self.update_url = "/api/versions?method=check"

    def get_online_versions(self):
        """
        Update Onling versions listing.
        """

        self.logger.debug("Checking for Online Information")

    def register_version(self, item_name, item_version, item_type):
        """
        Register a version item.
        """

        self.logger.debug("Registering %s item: %s %s" % (item_type, item_name, item_version))
        self.dict[item_name] = {
                                "name": item_name,
                                "version": item_version,
                                "type": item_type
                                }

    def register_EmbyUpdate(self):
        """
        Register core version items.
        """

        self.register_version("EmbyUpdate", EmbyUpdate_VERSION, "EmbyUpdate")

    def register_env(self):
        """
        Register env version items.
        """

        self.register_version("Python", sys.version, "env")
        if sys.version_info.major == 2 or sys.version_info < (3, 7):
            self.logger.error('Error: EmbyUpdate requires python 3.7+. Do NOT expect support for older versions of python.')

        opersystem = platform.system()
        self.register_version("Operating System", opersystem, "env")

        if opersystem in ["Linux", "Darwin"]:

            # Linux/Mac
            if os.getuid() == 0 or os.geteuid() == 0:
                self.logger.warning('Do not run EmbyUpdate with root privileges.')

        elif opersystem in ["Windows"]:

            # Windows
            if os.environ.get("USERNAME") == "Administrator":
                self.logger.warning('Do not run EmbyUpdate as Administrator.')

        else:
            self.logger.warning("Uncommon Operating System, use at your own risk.")

        cpu_type = platform.machine()
        self.register_version("CPU Type", cpu_type, "env")

        isdocker = is_docker()
        self.register_version("Docker", isdocker, "env")
