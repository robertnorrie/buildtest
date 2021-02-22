import os
from buildtest.config import load_settings
from buildtest.defaults import BUILDTEST_ROOT
from buildtest.executors.setup import BuildExecutor
from buildtest.menu.build import (
    build_phase,
    discover_buildspecs,
    parse_buildspecs,
    resolve_testdirectory,
    run_phase,
)

input_buildspecs = [os.path.join(BUILDTEST_ROOT, "tutorials", "pass_returncode.yml")]
included_bp, excluded_bp = discover_buildspecs(buildspec=input_buildspecs, debug=True)

configuration = load_settings()
testdir = resolve_testdirectory(configuration)
executor = BuildExecutor(configuration)

print("List of executors: ", executor.executors)
bp_filters = {"tags": None }
builders = parse_buildspecs(
    included_bp, test_directory=testdir, executor=executor, filters=bp_filters, rebuild=1, printTable=True
)

build_phase(builders, printTable=True)
run_phase(builders, executor, configuration, printTable=True)
