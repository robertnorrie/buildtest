############################################################################
#
#  Copyright 2017
#
#   https://github.com/HPC-buildtest/buildtest-framework
#
#  This file is part of buildtest.
#
#    buildtest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    buildtest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with buildtest.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################

"""
:author: Shahzeb Siddqiui
"""

import os
import argparse
import argcomplete
from framework.env import BUILDTEST_SHELLTYPES, config_opts
from framework.tools.system import systempackage_installed_list
from framework.tools.software import get_software_stack, get_toolchain_stack

syspkg_list = os.listdir(os.path.join(config_opts['BUILDTEST_CONFIGS_REPO'],"system"))
# adding "all" as parameter to run all system package test
syspkg_list.append("all")


pkglist = systempackage_installed_list()


software_list = get_software_stack()
toolchain_list = get_toolchain_stack()
class buildtest_menu():

        parser = {}

        def __init__(self):
        # reports an error, issue with import
        #software_list = get_unique_software_version(BUILDTEST_MODULE_EBROOT)

            parser = argparse.ArgumentParser(prog='buildtest', usage='%(prog)s [options]')
            parser.add_argument("-V", "--version", help="show program version number and exit",action="store_true")
            parser.add_argument("--logdir", help="Path to write buildtest logs. Override configuration BUILDTEST_LOGDIR")
            parser.add_argument("--testdir", help="Path to write buildtest tests. Overrides configuration BUILDTEST_TESTDIR")
            parser.add_argument("--ignore-easybuild", help="ignore if application is not built with easybuild",action="store_true")
            parser.add_argument("--show", help="show buildtest environment configuration", action="store_true")

            group1 = parser.add_argument_group('Basic Options', 'buildtest basic options')
            group1.add_argument("-mns", "--module-naming-scheme", help="Specify module naming scheme for easybuild apps", choices=["HMNS","FNS"])
            group1.add_argument("--scantest", help=""" Report all tests that can be built with buildtest by checking all available apps found
            in eb stack and system packages""", action="store_true")
            group1.add_argument("--clean-logs", help="delete buildtest logs",action="store_true")
            group1.add_argument("--clean-tests",help="delete testing directory",action="store_true")

            group2 = parser.add_argument_group('Find Options', 'buildtest options for finding software, toolchains, tests, yaml files')

            group2.add_argument("-lt", "--list-toolchain",help="retrieve a list of easybuild toolchain used for --toolchain option", action="store_true")
            group2.add_argument("-ls", "--list-unique-software",help="retrieve all unique software found in your module tree specified by BUILDTEST_MODULE_ROOT", action="store_true")
            group2.add_argument("-svr", "--software-version-relation", help="retrieve a relationship between software and version found in module files", action="store_true")
            group2.add_argument("-fc","--findconfig", help= """ Find buildtest YAML config files found in BUILDTEST_CONFIGS_REPO.
                                                 To find all yaml config files use -fc all """)
            group2.add_argument("-ft", "--findtest", help="""Find test scripts generated by buildtest defined by BUILDTEST_TESTDIR.
                                         To find all test scripts use -ft all """)
            group2.add_argument("-ecmt","--easyconfigs-in-moduletrees", help="Return a list of easyconfigs from a easybuild module tree",action="store_true")
            group2.add_argument("--diff-trees", help="Show difference between two module trees")

            group3 = parser.add_argument_group('Test Options', 'Options for building tests with buildtest')
            group3.add_argument("-s", "--software", help=" Specify software package to test", choices=software_list, metavar='INSTALLED-EASYBUILD-APPS')
            group3.add_argument("-t", "--toolchain",help=" Specify toolchain for the software package", choices=toolchain_list, metavar='INSTALLED-EASYBUILD-TOOLCHAINS')
            group3.add_argument("--shell", help=""" Select the type of shell when running test""", choices=BUILDTEST_SHELLTYPES)
            group3.add_argument("--system", help=""" Build test for system packages
                             To build all system package test use --system all """, choices=syspkg_list, metavar='SYSTEM-PACKAGE')
            group3.add_argument("--testset", help="Select the type of test set to run (Python, R, Ruby, Perl, Tcl, MPI)", choices=["Python","R","Ruby","Perl","Tcl","MPI"])


            group4 = parser.add_argument_group('YAML Options', 'Options for YAML configuration')
            group4.add_argument("--sysyaml", help = "generate binary test YAML configuration for system package", choices=pkglist, metavar='INSTALLED-SYSTEM-PACKAGE')
            group4.add_argument("--ebyaml", help = "generate binary test YAML configuration for easybuild package (Not Implemented)")


            group5 = parser.add_argument_group('Job Scheduler Options', 'Options for interacting with Job Scheduler')
            group5.add_argument("--job-template", help = "specify  job template file to create job submission script for the test to run with resource scheduler")
            group5.add_argument("--submitjob", help = "specify a directory or job script to submit to resource scheduler")

            group6 = parser.add_argument_group('Miscellaneous Options', 'rest of buildtest options')
            group6.add_argument("--runtest", help="Run the test interactively through runtest.py", action="store_true")
            self.parser = parser

        #argcomplete.autocomplete(parser)
        #args = parser.parse_args()

        #return vars(args)


        def parse_options(self):
                """ return argument as a dictionary"""

                argcomplete.autocomplete(self.parser)
                args = self.parser.parse_args()
                return args
