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

        self.release_version = str(self.config.dict["emby"]["release_version"]).lower()

    def update_check(self):

        self.logger.debug("Checking for current release of Emby")
        if self.embyupdate_release_version in ["prerelease"]:
            prerelease = True
        else:
            prerelease = False
        onlineversion = self.get_current_github_release("mediabrowser", "Emby.releases", prerelease)
        self.logger.debug("Online release of Emby is %s" % onlineversion)
