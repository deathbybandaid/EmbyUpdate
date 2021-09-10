# coding=utf-8
import json

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

        self.release_url = "https://api.github.com/repos/mediabrowser/Emby.releases/releases"
        self.release_version = self.config.dict["main"]["release_version"]

    def update_check(self):

        self.logger.debug("Checking Emby Releases.")
        try:

            response = self.web.get(self.release_url)
            updatejson = json.loads(response.text)

            # Here we search the github API response for the most recent version of beta or stable depending on what was chosen
            # above.
            for i, entry in enumerate(updatejson):

                if self.release_version == 'beta':

                    if entry["prerelease"] is True:
                        onlineversion = entry["tag_name"]
                        versiontype = "beta"
                        break

                else:

                    if entry["prerelease"] is False:
                        onlineversion = entry["tag_name"]
                        versiontype = "stable"
                        break

        except Exception as e:
            self.logger.error("EmbyUpdate: We didn't get an expected response from the github api, script is exiting!")
            self.logger.error("EmbyUpdate: Here's the error we got: %s" % e)
