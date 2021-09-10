# import os
import argparse
import pathlib

from EmbyUpdate import EmbyUpdate_VERSION
# import EmbyUpdate.exceptions
# import EmbyUpdate.config
# import EmbyUpdate.logger
# import EmbyUpdate.versions

ERR_CODE = 1


def build_args_parser(script_dir):
    """
    Build argument parser for EmbyUpdate.
    """

    parser = argparse.ArgumentParser(description='EmbyUpdate')
    parser.add_argument('-c', '--config', dest='cfg', type=str, default=pathlib.Path(script_dir).joinpath('config.ini'), required=False, help='configuration file to load.')
    parser.add_argument('--setup', dest='setup', type=str, required=False, nargs='?', const=True, default=False, help='Setup Configuration file.')
    return parser.parse_args()


def run(settings, logger, script_dir, versions, deps):
    """
    Create EmbyUpdate and fHDHH_web objects, and run threads.
    """

    try:

        print("Doing Stuff Now")

    except KeyboardInterrupt:
        return ERR_CODE

    return ERR_CODE


def start(args, script_dir, deps):
    """
    Get Configuration for EmbyUpdate and start.
    """

    # try:
    #    settings = EmbyUpdate.config.Config(args, script_dir)
    # except EmbyUpdate.exceptions.ConfigurationError as e:
    #    print(e)
    #    return ERR_CODE

    # Setup Logging
    # logger = EmbyUpdate.logger.Logger(settings)
    # settings.logger = logger

    # logger.noob("Loading EmbyUpdate %s with EmbyUpdate_web %s" % (EmbyUpdate_VERSION))
    # logger.info("Importing Core config values from Configuration File: %s" % settings.config_file)

    # logger.debug("Logging to File: %s" % os.path.join(settings.internal["paths"]["logs_dir"], '.EmbyUpdate.log'))

    # Continue non-core settings setup
    # settings.secondary_setup()

    # Setup Version System
    # versions = EmbyUpdate.versions.Versions(settings, logger)

    # return run(settings, logger, script_dir, versions, deps)


def config_setup(args, script_dir):
    """
    Setup Config file.
    """

    # settings = EmbyUpdate.config.Config(args, script_dir)
    # EmbyUpdate.plugins.PluginsHandler(settings)
    # settings.setup_user_config()
    return ERR_CODE


def main(script_dir, deps):
    """
    EmbyUpdate run script entry point.
    """

    try:
        args = build_args_parser(script_dir)

        if args.setup:
            return config_setup(args, script_dir)  # TODO

        # return start(args, script_dir, deps)

    except KeyboardInterrupt:
        print("\n\nInterrupted")
        return ERR_CODE

    return ERR_CODE


if __name__ == '__main__':
    """
    Trigger main function.
    """
    main()