# coding=utf-8

EmbyUpdate_VERSION = "v3.2"


class EmbyUpdate_INT_OBJ():

    def __init__(self, settings, logger, versions, web, deps):
        """
        An internal catalogue of core methods.
        """

        self.version = EmbyUpdate_VERSION
        self.versions = versions
        self.config = settings
        self.logger = logger
        self.web = web
        self.deps = deps


class EmbyUpdate_OBJ():

    def __init__(self, settings, logger, versions, web, deps):
        """
        The Core Backend.
        """

        logger.info("Initializing EmbyUpdate Core Functions.")
        self.embyupdate = EmbyUpdate_INT_OBJ(settings, logger, versions, web, deps)

    def __getattr__(self, name):
        """
        Quick and dirty shortcuts. Will only get called for undefined attributes.
        """

        if hasattr(self.embyupdate, name):
            return eval("self.embyupdate.%s" % name)
