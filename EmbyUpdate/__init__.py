# coding=utf-8

import time
import subprocess

EmbyUpdate_VERSION = "v3.2"


class EmbyUpdate_OBJ():

    def __init__(self, settings, logger, versions, web, deps):
        """
        The Core Backend.
        """

        self.version = EmbyUpdate_VERSION
        self.versions = versions
        self.config = settings
        self.logger = logger
        self.web = web
        self.deps = deps

        self.emby_release_version = str(self.config.dict["emby"]["release_version"]).lower()
        self.emby_installed_version = self.config.dict["emby"]["installed_version"]
        self.serverstop = self.config.dict["emby"]["serverstop"]
        self.serverstart = self.config.dict["emby"]["serverstart"]

    def update_check(self):

        print(self.versions.dict)

        self.logger.debug("Checking for current release of Emby")
        if self.emby_release_version in ["prerelease"]:
            prerelease = True
        else:
            prerelease = False
        onlineversion = self.versions.get_current_github_release("mediabrowser", "Emby.releases", prerelease)
        self.logger.debug("Online release of Emby is %s" % onlineversion)

        if not self.emby_installed_version:
            # TODO find a better way to get currently installed version
            # maybe find a list of default install paths
            self.logger.info("Emby is either not installed, or this is the first run of EmbyUpdate.")
        else:
            self.logger.info("Current Installed version of Emby is %s. Online version is %s." % (self.emby_installed_version, onlineversion))

        if not self.emby_installed_version or self.emby_installed_version != self.emby_release_version:
            self.logger.info("Starting Update...")
        else:
            self.logger.info("Emby is up to date, Not running update.")

    def update_run(self):

        # This will stop the server on a systemd distro if it's been set to true above
        if self.serverstop == "True":
            print("Stopping Emby server.....")
            stopreturn = subprocess.call("systemctl stop emby-server", shell=True)
            time.sleep(3)
            if stopreturn > 0:
                self.logger.error("Server Stop failed! Non-critical error! Investigate if needed.")

            print("Emby Server Stopped...")

        return
