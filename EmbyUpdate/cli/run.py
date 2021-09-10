import os
import argparse
import pathlib

from EmbyUpdate import EmbyUpdate_VERSION, EmbyUpdate_OBJ
import EmbyUpdate.config
import EmbyUpdate.logger
import EmbyUpdate.versions
import EmbyUpdate.web

ERR_CODE = 1
ERR_CODE_NO_RESTART = 2


def build_args_parser(script_dir):
    """
    Build argument parser for EmbyUpdate.
    """

    parser = argparse.ArgumentParser(description='EmbyUpdate')
    parser.add_argument('-c', '--config', dest='cfg', type=str, default=pathlib.Path(script_dir).joinpath('config.ini'), required=False, help='configuration file to load.')
    parser.add_argument('--setup', dest='setup', type=str, required=False, nargs='?', const=True, default=False, help='Setup Configuration file.')
    parser.add_argument('-v', '--version', dest='version', type=str, required=False, nargs='?', const=True, default=False, help='Displays Version Number.')
    return parser.parse_args()


def run(settings, logger, script_dir, versions, deps, web):
    """
    Run EmbyUpdate.
    """

    embyupdate = EmbyUpdate_OBJ(settings, logger, versions, web, deps)
    embyupdate.update_check()

    return ERR_CODE


def start(args, script_dir, deps):
    """
    Get Configuration for EmbyUpdate and start.
    """

    try:
        settings = EmbyUpdate.config.Config(args, script_dir)
    except EmbyUpdate.exceptions.ConfigurationError as e:
        print(e)
        return ERR_CODE

    # Setup Logging
    logger = EmbyUpdate.logger.Logger(settings)
    settings.logger = logger

    logger.info("Loading EmbyUpdate %s" % (EmbyUpdate_VERSION))
    logger.info("Importing Core config values from Configuration File: %s" % settings.config_file)

    logger.debug("Logging to File: %s" % os.path.join(settings.internal["paths"]["logs_dir"], '.EmbyUpdate.log'))

    logger.debug("Setting Up shared Web Requests system.")
    web = EmbyUpdate.web.WebReq()

    # Setup Version System
    versions = EmbyUpdate.versions.Versions(settings, logger, web)

    return run(settings, logger, script_dir, versions, deps, web)


def config_setup(args, script_dir):
    """
    Setup Config file.
    """

    settings = EmbyUpdate.config.Config(args, script_dir)
    settings.setup_user_config()
    return ERR_CODE


def main(script_dir, deps):
    """
    EmbyUpdate run script entry point.
    """

    try:
        args = build_args_parser(script_dir)

        if args.version:
            print(EmbyUpdate_VERSION)
            return ERR_CODE

        if args.setup:
            return config_setup(args, script_dir)  # TODO

        return start(args, script_dir, deps)

    except KeyboardInterrupt:
        print("\n\nInterrupted")
        return ERR_CODE

    return ERR_CODE


if __name__ == '__main__':
    """
    Trigger main function.
    """
    main()
