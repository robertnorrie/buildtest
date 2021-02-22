"""Entry point for buildtest"""

import os
import shutil
import sys
import tempfile
from buildtest.config import check_settings, resolve_settings_file
from buildtest.defaults import var_root, BUILDTEST_USER_HOME
from buildtest.menu import BuildTestParser
from buildtest.menu.build import func_build_subcmd
from buildtest.system import system
from buildtest.log import init_logfile, streamlog
from buildtest.utils.file import create_dir, resolve_path

# column width for linewrap for argparse library
os.environ["COLUMNS"] = "120"


def main():
    """Entry point to buildtest."""

    # create a temporary file to store logfile and we don't delete file by setting 'delete=False'
    # by default tempfile will delete file upon exit.
    tf = tempfile.NamedTemporaryFile(prefix="buildtest_", delete=False, suffix=".log")
    dest_logfile = tf.name

    logger = init_logfile(dest_logfile)
    logger.info("Starting buildtest log")

    create_dir(BUILDTEST_USER_HOME)
    create_dir(var_root)

    # Create a build test system, and check requirements
    # BuildTestSystem()
    system.check()

    parser = BuildTestParser()
    args = parser.parse_options()

    if args.debug:
        streamlog(args.debug)

    # invoking load_settings will attempt to initialize buildtest settings and
    # load the schema
    settings_file = resolve_settings_file()
    logger.info(f"Processing buildtest configuration file: {settings_file}")
    buildtest_configuration = check_settings(settings_file, retrieve_settings=True)

    if args.subcommands == "build":
        func_build_subcmd(args, buildtest_configuration)
    else:
        if args.subcommands and args.func:
            args.func(args)

    logdir = buildtest_configuration.get("logdir")

    if not logdir:
        print(f"Writing Logfile to: {dest_logfile}")
        sys.exit(0)

    logdir = resolve_path(logdir, exist=False)
    if logdir:
        create_dir(logdir)
        fname = os.path.basename(dest_logfile)
        logpath = os.path.join(logdir, fname)
        shutil.copy2(dest_logfile, logpath)

        print(f"Writing Logfile to: {logpath}")
    else:
        print(f"Writing Logfile to: {dest_logfile}")


if __name__ == "__main__":
    main()
