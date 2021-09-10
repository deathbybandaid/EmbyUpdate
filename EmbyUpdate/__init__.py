# coding=utf-8

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

    def update_check(self):

        self.logger.debug("Checking for current release of Emby")
        if self.emby_release_version in ["prerelease"]:
            prerelease = True
        else:
            prerelease = False
        onlineversion = self.versions.get_current_github_release("mediabrowser", "Emby.releases", prerelease)
        self.logger.debug("Online release of Emby is %s" % onlineversion)

        if not self.emby_installed_version:
            self.logger.info("Emby is either not installed, or this is the first run of EmbyUpdate.")
        else:
            self.logger.info("Current Installed version of Emby is %s. Online version is %s." % (self.emby_installed_version, onlineversion))
