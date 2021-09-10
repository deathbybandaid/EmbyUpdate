import os
import sys
import platform
import json

from EmbyUpdate import EmbyUpdate_VERSION
from EmbyUpdate.tools import is_docker


class Versions():
    """
    EmbyUpdate versioning management system.
    """

    def __init__(self, settings, logger, web):
        self.logger = logger
        self.web = web
        self.config = settings

        self.dict = {}

        self.register_EmbyUpdate()

        self.register_env()

        self.embyupdate_release_version = str(self.config.dict["main"]["release_version"]).lower()

        self.get_online_versions()

    def get_current_github_release(self, owner, repository, prerelease):

        github_releases_url = "https://api.github.com/repos/%s/%s/releases" % (owner, repository)

        # Now we're just going to see what the latest version is!
        try:

            response = self.web.get(github_releases_url)
            updatejson = json.loads(response.text)

            # Here we search the github API response for the most recent version of beta or stable depending on what was chosen
            # above.
            for i, entry in enumerate(updatejson):

                if prerelease:

                    if entry["prerelease"] is True:
                        onlineversion = entry["tag_name"]
                        break

                else:

                    if entry["prerelease"] is False:
                        onlineversion = entry["tag_name"]
                        break

        except Exception as e:
            self.logger.error("We didn't get an expected response from the github api.")
            self.logger.error("Here's the error we got: %s" % e)
            onlineversion = None

        return onlineversion

    def get_online_versions(self):
        """
        Update Onling versions listing.
        """

        self.logger.debug("Checking for current release of EmbyUpdate")
        if self.embyupdate_release_version in ["prerelease"]:
            prerelease = True
        else:
            prerelease = False
        onlineversion = self.get_current_github_release("doonze", "Embyupdate", prerelease)
        self.logger.debug("Online release of EmbyUpdate is %s" % onlineversion)

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
