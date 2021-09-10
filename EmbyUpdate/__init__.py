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

    def update_check(self):

        response = self.web.get(self.release_url)
        updatejson = json.loads(response.text)
        print(updatejson)
