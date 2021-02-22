"""
buildtest menu: include functions to build, get test configurations, and 
interact with a global configuration for buildtest.
"""
import argcomplete
import argparse

from buildtest import BUILDTEST_VERSION
from buildtest.docs import buildtestdocs, schemadocs
from buildtest.menu.buildspec import func_buildspec_find
from buildtest.menu.config import (
    func_config_summary,
    func_config_validate,
    func_config_view,
)
from buildtest.menu.compilers import func_compiler_find, func_config_compiler
from buildtest.menu.report import func_report
from buildtest.menu.schema import func_schema
from buildtest.menu.inspect import func_inspect
from buildtest.schemas.defaults import schema_table


def handle_kv_string(val):
    """This method is used as type field in --filter argument in ``buildtest buildspec find``.
       This method returns a dict of key,value pair where input is in format
       key1=val1,key2=val2,key3=val3

       :param val: input value
       :type val: str
       :return: dictionary of key/value pairs
       :rtype: dict
    """

    kv_dict = {}

    if "," in val:
        args = val.split(",")
        for kv in args:
            if "=" in kv:
                key, value = kv.split("=")[0], kv.split("=")[1]
                kv_dict[key] = value
            else:
                raise argparse.ArgumentTypeError("Must specify k=v")

    else:
        if "=" in val:
            key, value = val.split("=")[0], val.split("=")[1]
            kv_dict[key] = value

    return kv_dict


def positive_number(value):
    if int(value) <= 0 or int(value) > 50:
        raise argparse.ArgumentTypeError(
            f"{value} must be a positive number between [1-50]"
        )
    return value


class BuildTestParser:
    def __init__(self):
        epilog_str = (
            "Documentation: " + "https://buildtest.readthedocs.io/en/latest/index.html"
        )
        description_str = (
            "buildtest is a HPC testing framework for building and executing"
            + "tests. Buildtest comes with a set of json-schemas used to write "
            + "test configuration (Buildspecs) in YAML to generate test scripts."
        )

        self.parser = argparse.ArgumentParser(
            prog="buildtest",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=description_str,
            usage="%(prog)s [options] [COMMANDS]",
            epilog=epilog_str,
        )
        self.subparser_dict = {
            "build": "Options for building test scripts",
            "buildspec": "Command options for buildspecs",
            "report": "Show report for test results",
            "schema": "Commands for viewing buildtest schemas",
            "config": "Buildtest Configuration Menu",
            "inspect": "Inspect details for test from test report",
            "docs": "Open buildtest docs in browser",
            "schemadocs": "Open buildtest schema docs in browser",
        }

        self.main_menu()
        self.build_menu()
        self.buildspec_menu()
        self.report_menu()
        self.inspect_menu()
        self.schema_menu()
        self.config_menu()

    def main_menu(self):
        """This method adds argument to ArgumentParser to main menu of buildtest"""

        command_description = ""
        for k, v in self.subparser_dict.items():
            command_description += "\n {:<30} {:<30}".format(k, v)

        self.subparsers = self.parser.add_subparsers(
            title="COMMANDS", description=command_description, dest="subcommands"
        )

        self.parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=f"""buildtest version {BUILDTEST_VERSION}""",
        )
        self.parser.add_argument(
            "-d",
            "--debug",
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help="Enable debugging messages.",
        )
        parser_docs = self.subparsers.add_parser("docs")
        parser_docs.set_defaults(func=buildtestdocs)

        parser_schemadocs = self.subparsers.add_parser("schemadocs")
        parser_schemadocs.set_defaults(func=schemadocs)

    def parse_options(self):
        """This method parses the argument from ArgumentParser class and returns
        the arguments. We store extra (non parsed arguments) with the class if
        they are needed.

        :return: return a parsed dictionary returned by ArgumentParser
        :rtype: dict
        """

        argcomplete.autocomplete(self.parser)
        args, extra = self.parser.parse_known_args()
        self.extra = extra

        return args

    def build_menu(self):
        """This method implements the ``buildtest build`` command"""

        parser_build = self.subparsers.add_parser("build")

        ##################### buildtest build  ###########################

        parser_build.add_argument(
            "-b",
            "--buildspec",
            help="Specify a Buildspec (YAML) file to build and run the test.",
            action="append",
        )

        parser_build.add_argument(
            "-x",
            "--exclude",
            action="append",
            help="Exclude one or more configs from processing. Configs can be files or directories.",
        )

        parser_build.add_argument(
            "-t",
            "--tags",
            action="append",
            type=str,
            help="Discover buildspecs by tags found in buildspec cache",
        )
        parser_build.add_argument(
            "-ft",
            "--filter-tags",
            action="append",
            type=str,
            help="Filter buildspecs by tags when building tests.",
        )

        parser_build.add_argument(
            "-e",
            "--executor",
            action="append",
            type=str,
            help="Discover buildspecs by executor name found in buildspec cache",
        )
        parser_build.add_argument(
            "-s",
            "--stage",
            help="control behavior of buildtest build",
            choices=["parse", "build"],
        )

        parser_build.add_argument(
            "--testdir",
            help="specify a custom test directory. By default, use .buildtest in $PWD.",
        )
        parser_build.add_argument(
            "--rebuild",
            type=positive_number,
            help="Rebuild test X number of times. Must be a positive number between [1-50]",
        )

    def buildspec_menu(self):
        """This method implements ``buildtest buildspec`` command"""

        # ####################### buildtest buildspec  ########################
        parser_buildspec = self.subparsers.add_parser("buildspec")

        subparsers_buildspec = parser_buildspec.add_subparsers(
            description="Commands options for Buildspecs"
        )
        buildspec_find = subparsers_buildspec.add_parser(
            "find", help="find all buildspecs"
        )
        buildspec_find.add_argument(
            "--root",
            help="Specify root buildspecs (directory) path to load buildspecs into buildspec cache.",
            type=str,
            action="append",
        )

        buildspec_find.add_argument(
            "-r",
            "--rebuild",
            help="Rebuild buildspec cache and find all buildspecs again",
            action="store_true",
        )
        buildspec_find.add_argument(
            "-t", "--tags", help="List all available tags", action="store_true"
        )
        buildspec_find.add_argument(
            "-bf",
            "--buildspec-files",
            help="Get all buildspec files from cache",
            action="store_true",
        )
        buildspec_find.add_argument(
            "-e",
            "--executors",
            help="get all unique executors from buildspecs",
            action="store_true",
        )
        buildspec_find.add_argument(
            "-p", "--paths", help="print all root buildspec paths", action="store_true"
        )
        buildspec_find.add_argument(
            "--group-by-tags", action="store_true", help="Group tests by tag name"
        )
        buildspec_find.add_argument(
            "--group-by-executor",
            action="store_true",
            help="Group tests by executor name",
        )
        buildspec_find.add_argument(
            "-m",
            "--maintainers",
            help="Get all maintainers for all buildspecs",
            action="store_true",
        )
        buildspec_find.add_argument(
            "-mb",
            "--maintainers-by-buildspecs",
            help="Show maintainers breakdown by buildspecs",
            action="store_true",
        )
        buildspec_find.add_argument(
            "--filter",
            type=handle_kv_string,
            help="Filter buildspec cache with filter fields in format --filter key1=val1,key2=val2",
        )
        buildspec_find.add_argument(
            "--format",
            help="Format buildspec cache with format fields in format --format field1,field2,...",
        )
        buildspec_find.add_argument(
            "--helpfilter",
            action="store_true",
            help="Show Filter fields for --filter option for filtering buildspec cache output",
        )
        buildspec_find.add_argument(
            "--helpformat",
            action="store_true",
            help="Show Format fields for --format option for formatting buildspec cache output",
        )
        buildspec_find.set_defaults(func=func_buildspec_find)

    def config_menu(self):
        """This method adds argparse argument for ``buildtest config``"""

        parser_config = self.subparsers.add_parser("config")

        subparsers_config = parser_config.add_subparsers(
            description="buildtest configuration"
        )
        compiler_config = subparsers_config.add_parser(
            "compilers", help="search or find compilers "
        )
        subparsers_compiler_find = compiler_config.add_subparsers(
            description="Find new compilers and add them to detected compiler section"
        )
        compiler_find = subparsers_compiler_find.add_parser(
            "find", help="Find compilers"
        )
        compiler_find.add_argument(
            "-d",
            "--debug",
            help="Display Debugging output when finding compilers",
            action="store_true",
        )

        parser_config_view = subparsers_config.add_parser(
            "view", help="View Buildtest Configuration File"
        )
        parser_config_validate = subparsers_config.add_parser(
            "validate", help="Validate buildtest settings file with schema."
        )

        parser_config_summary = subparsers_config.add_parser(
            "summary", help="Provide summary of buildtest settings."
        )

        compiler_config.add_argument(
            "-j",
            "--json",
            action="store_true",
            help="List compiler details in JSON format",
        )
        compiler_config.add_argument(
            "-y",
            "--yaml",
            action="store_true",
            help="List compiler details in YAML format",
        )
        compiler_config.add_argument(
            "-l", "--list", action="store_true", help="List all compilers "
        )

        parser_config_view.set_defaults(func=func_config_view)
        parser_config_validate.set_defaults(func=func_config_validate)
        parser_config_summary.set_defaults(func=func_config_summary)

        compiler_config.set_defaults(func=func_config_compiler)
        compiler_find.set_defaults(func=func_compiler_find)

    def report_menu(self):
        """This method implements the ``buildtest report`` command options"""

        parser_report = self.subparsers.add_parser("report")
        parser_report.add_argument(
            "--helpformat", action="store_true", help="List of available format fields"
        )
        parser_report.add_argument(
            "--format",
            help="format field for printing purposes. For more details see --helpformat for list of available fields. Fields must be separated by comma (--format <field1>,<field2>,...)",
        )
        parser_report.add_argument(
            "--filter",
            type=handle_kv_string,
            help="Filter report by filter fields. The filter fields must be set in format: --filter key1=val1,key2=val2,...",
        )
        parser_report.add_argument(
            "--helpfilter",
            action="store_true",
            help="Report a list of filter fields to be used with --filter option",
        )
        ##################### buildtest report   ###########################

        parser_report.set_defaults(func=func_report)

    def inspect_menu(self):
        """This method builds menu for `buildtest inspect` """

        parser_inspect = self.subparsers.add_parser("inspect")
        parser_inspect.add_argument("test", help="select unique test")
        parser_inspect.set_defaults(func=func_inspect)

    def schema_menu(self):
        """This method adds argparse argument for ``buildtest show``"""

        # ################### buildtest schema  ########################
        parser_schema = self.subparsers.add_parser("schema")

        parser_schema.add_argument(
            "-n",
            "--name",
            help="show schema by name (e.g., script)",
            metavar="Schema Name",
            choices=schema_table["names"],
        )
        parser_schema.add_argument(
            "-e", "--example", action="store_true", help="Show schema examples",
        )
        parser_schema.add_argument(
            "-j", "--json", action="store_true", help="Display json schema file"
        )
        parser_schema.add_argument(
            "-v",
            "--validate",
            action="store_true",
            help="Validate all schema examples with corresponding schemafile",
        )
        parser_schema.set_defaults(func=func_schema)
