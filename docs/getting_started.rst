.. _Getting_Started:

Getting Started
================

This guide will get you familiar with buildtest command line interface. Once
you complete this section, you can proceed to :ref:`writing buildspecs <writing_buildspecs>`
section where we will cover how to write buildspecs.

Once you install buildtest, you should find the `buildtest` command in your **$PATH**.
You can check the path to buildtest command by running::

      $ which buildtest

If you don't see buildtest go back and :ref:`install buildtest <Setup>`.


When you clone buildtest, you also get a set of buildspecs that you can run on your
system. The ``buildtest build`` command is used for building and running tests.
Buildtest will read one or more buildspecs file that adheres to one of the
buildtest schemas. For a complete list of build options, run ``buildtest build --help``

Build Usage
------------

.. program-output:: cat docgen/buildtest_build_--help.txt

Building a Test
----------------

To build a test, we use the ``--buildspec`` or short option ``-b`` to specify the
path to buildspec file. Let's see some examples, first we specify a full path to buildspec file.
In this example, buildtest will :ref:`discover buildspecs <discover_buildspecs>` followed by
parsing the test with appropriate schema and generate a shell script that is run
by buildtest. You can learn more about :ref:`build and test process <build_and_test_process>`.

.. program-output:: cat docgen/getting_started/buildspec-abspath.txt

.. Note::
    buildtest will only read buildspecs with ``.yml`` extension, if you specify a
    ``.yaml`` it will be ignored by buildtest.

The ``--buildspec`` option can be used to specify a file or directory path. If you want
to build multiple buildspecs in a directory you can specify the directory path
and buildtest will recursively search for all ``.yml`` files. In the next example,
we build all tests in directory **general_tests/configuration**.

.. program-output:: cat docgen/getting_started/buildspec-directory.txt

Building Multiple Buildspecs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can append ``-b`` option to build multiple buildspecs in the same
command. Buildtest will discover buildspecs for every argument (``-b``) and accumulate
a list of buildspecs to run. In this example, we instruct buildtest to build
a buildspec file and all buildspecs in a directory path.

.. program-output:: cat docgen/getting_started/multi-buildspecs.txt

.. _exclude_buildspecs:

Excluding Buildspecs
~~~~~~~~~~~~~~~~~~~~~

So far we learned how to build buildspecs by file and directory path using the ``-b``
option. Next, we will discuss how one may exclude buildspecs which behaves similar to
``-b`` option. You can exclude buildspecs via ``--exclude`` or short option ``-x``
which can be useful when you want to exclude certain files or sub directory.

For example we can build all buildspecs in ``tutorials`` but exclude file ``tutorials/vars.yml``
by running::

    $ buildtest build -b tutorials -x tutorials/vars.yml

buildtest will discover all buildspecs and then exclude any buildspecs specified
by ``-x`` option. You can specify ``-x`` multiple times just like ``-b`` option.

For example, we can undo discovery by passing same option to ``-b`` and ``-x``  as follows::

    $ buildtest build -b tutorials/ -x tutorials/
    There are no Buildspec files to process.

Buildtest will stop immediately if there are no Buildspecs to process, this is
true if you were to specify files instead of directory.

In this example, we build all buildspecs in a directory but exclude two files. Buildtest
will report the excluded buildspecs in the output.

.. program-output:: cat docgen/getting_started/exclude_buildspecs.txt
.. _build_by_tags:

Building By Tags
~~~~~~~~~~~~~~~~~

buildtest can perform builds by tags by using ``--tags`` or short option (``-t``).
In order to use this feature, buildtest must load buildspecs in :ref:`cache <find_buildspecs>` which can be run
via ``buildtest buildspec find``.

To build all tutorials tests you can perform ``buildtest build --tags tutorials``.
In buildspec file, there is a field ``tags: [tutorials]`` to classify tests.
buildtest will read the cache file ``var/buildspec-cache.json`` and see which
buildspecs have a matching tag. You should run ``buildtest buildspec find``
atleast once, in order to detect cache file.

.. program-output::  cat docgen/getting_started/tags.txt

You can build by multiple tags by specifying ``--tags`` multiple times. In next
example we build all tests with tag name ``pass`` and ``python``.

.. program-output:: cat docgen/getting_started/multi-tags.txt

When multiple tags are specified, we search each tag independently and if it's
found in the buildspec cache we retrieve the buildspec file and add file to queue.
This queue is a list of buildspecs that buildtest will process (i.e ``parse``, ``build``, ``run``).
You can :ref:`query tags <buildspec_tags>` from buildspecs cache to see all available
tags by running ``buildtest buildspec find --tags``.

.. Note:: The ``--tags`` is used for discovering buildspec file and not filtering tests
   by tag. If you want to filter tests by tags use ``--filter-tags``.

The ``--filter-tags`` or short option ``-ft`` is used for filtering tests by
tag name. The ``--filter-tags`` is used in conjunction with other options like
``--buildspec``, ``--tags``, or ``--executor`` for discovering buildspecs.
Let's rerun the previous example and filter tests by ``pass``. Now we only see
tests built with tagname ``pass`` and all remaining tests were ignored.

.. program-output:: cat docgen/getting_started/combine-filter-tags-buildspec.txt

The ``--filter-tags`` option can be appended multiple times to filter tests by
multiple tags. If buildtest detects no tests were found when filtering tests by
tag name then buildtest will report a message. In example below we see no buildspecs
were found with tag name ``compile`` in the test.


.. program-output:: cat docgen/getting_started/filter-tags-nobuildspecs.txt

You can combine ``--tags`` with ``--buildspec`` to discover buildspecs in a single command.
buildtest will query tags and buildspecs independently and combine all discovered
buildspecs together.

.. program-output:: cat docgen/getting_started/combine-tags-buildspec.txt

As you may see, there are several ways to build buildspecs with buildtest. Tags is
great way to build a whole collection of tests if you don't know path to all the files. You can
specify multiple tags per buildspecs to classify how test can be run.

.. _build_by_executor:

Building by Executors
~~~~~~~~~~~~~~~~~~~~~~

Every buildspec is associated to an executor which is responsible for running the test.
You can instruct buildtest to run all tests by given executor via ``--executor`` option.
For instance, if you want to build all test associated to executor ``local.sh`` you can run::

  $ buildtest build --executor local.sh

buildtest will query buildspec cache for the executor name and retrieve a list of
buildspecs with matching executor name. To see a list of available executors in
buildspec cache see :ref:`querying buildspec executor <buildspec_executor>`.

.. Note:: By default all tests are run in buildspec file.  The ``buildtest build --executor`` option discovers
   buildspecs if one of the test matches the executor name. The ``--executor`` option
   is **not filtering on test level**  like ``--filter-tags`` option.

In this example we run all tests that are associated to `local.sh` executor. Notice how
buildtest skips tests that don't match executor **local.sh** even though they were
discovered in buildspec file.

.. program-output:: cat docgen/getting_started/single-executor.txt

We can append arguments to ``--executor`` to search for multiple executors by
specifying ``--executor <name1> --executor <name2>``. In next example we search
all tests associated with ``local.sh`` and ``local.bash`` executor.

.. Note:: If you specify multiple executors, buildtest will combine the executors
   into list, for example ``--executor local.bash --executor local.sh`` is converted
   into a list (executor filter) - ``[local.bash, local.sh]``, and buildtest will
   skip any test whose ``executor`` field in testname doesn't belong to executor
   filter list are skipped.

.. program-output:: cat docgen/getting_started/multi-executor.txt

.. _discover_buildspecs:

Discover Buildspecs
--------------------

Now, let's discuss how buildtest discovers buildspecs since there are several ways to build
buildspecs.

The buildspec search resolution is described as follows:

- If file or directory specified by ``-b`` option doesn't exist we exit immediately.

- If buildspec path is a directory, traverse directory recursively to find all ``.yml`` extensions

- If buildspec path is a file, check if file extension is not ``.yml``,  exit immediately

- If user specifies ``--tags`` or ``--executor`` we search in buildspec cache to discover buildspecs.

Shown below is a diagram on how buildtest discovers buildspecs. The user can build buildspecs
by ``--buildspec``, :ref:`--tags <build_by_tags>`, or :ref:`--executor <build_by_executor>`
which will discover the buildspecs. You can :ref:`exclude buildspecs <exclude_buildspecs>`
using ``--exclude`` option which is processed after discovering buildspecs. The
excluded buildspecs are removed from list if found and final list of buildspecs
is processed.

.. image:: _static/DiscoverBuildspecs.jpg
   :scale: 75 %


Control builds by Stages
-------------------------

We can control behavior of ``buildtest build`` command to stop at certain phase
using ``--stage`` option. The **--stage** option accepts ``parse`` or ``build``, which
will instruct buildtest to stop at parse or build phase of the pipeline.

Buildtest will validate all the buildspecs in the parse stage, so you can
instruct buildtest to stop at parse stage via ``--stage=parse``. This can be useful
when debugging buildspecs that are invalid. In this example below, we instruct
buildtest to stop after parse stage.

.. program-output:: cat docgen/getting_started/stage_parse.txt

Likewise, if you want to troubleshoot your test script without running them you can
use ``--stage=build`` which will stop after build phase. This can
be used when you are writing buildspec to troubleshoot how test is generated.
In this next example, we inform buildtest to stop after build stage.

.. program-output:: cat docgen/getting_started/stage_build.txt

.. _invalid_buildspecs:

Invalid Buildspecs
--------------------

buildtest will skip any buildspecs that fail to validate, in that case
the test script will not be generated. Here is an example where we have an invalid
buildspec.

.. program-output:: cat docgen/getting_started/invalid-buildspec.txt

buildtest may skip tests from running if buildspec specifies an invalid
executor name since buildtest needs to know this in order to delegate test
to Executor class responsible for running the test. Here is an example
where test failed to run since we provided invalid executor.

.. program-output:: cat docgen/getting_started/invalid-executor.txt

Rebuild Tests
--------------

buildtest can rebuild tests using the ``--rebuild`` option which can be useful if
you want to test a particular test multiple times. The rebuild option works across
all discovered buildspecs and create a new test instance (unique id) and test directory
path. To demonstrate we will build ``tutorials/python-shell.yml`` three times using
``--rebuild=3``.

.. program-output:: cat docgen/getting_started/rebuild.txt

The rebuild works with all options including: ``--buildspec``, ``--exclude``, ``--tags``
and ``--executors``.

In the next example we rebuild tests by discovering all tags that contain **fail**.

.. program-output:: cat docgen/getting_started/rebuild-tags.txt

The rebuild option expects a range between **1-50**, the ``--rebuild=1`` is equivalent
to running without ``--rebuild`` option. We set a max limit for rebuild option to
avoid system degredation due to high workload.

If you try to exceed this bound you will get an error such as::

    $ buildtest build -b tutorials/pass_returncode.yml --rebuild 51
    usage: buildtest [options] [COMMANDS] build [-h] [-b BUILDSPEC] [-x EXCLUDE] [--tags TAGS] [-e EXECUTOR]
                                                [-s {parse,build}] [-t TESTDIR] [--rebuild REBUILD] [--settings SETTINGS]
    buildtest [options] [COMMANDS] build: error: argument --rebuild: 51 must be a positive number between [1-50]

Buildspecs Interface
----------------------

Now that we learned how to build tests, in this section we will discuss how one can
query a buildspec cache. In buildtest, one can load all buildspecs which is equivalent
to validating all buildspecs with the appropriate schema. Buildtest will ignore all
invalid buildspecs and store them in a separate file.

The ``buildtest buildspec find`` command is used for finding buildspecs from buildspec
cache. This command is also used for generating the buildspec cache. Shown below is a list of options for
``buildtest buildspec find``.

.. program-output:: cat docgen/buildtest_buildspec_find_--help.txt

.. _find_buildspecs:

Finding Buildspecs
~~~~~~~~~~~~~~~~~~~~

To find all buildspecs run ``buildtest buildspec find`` which will discover
all buildspecs in all repos by recursively finding all `.yml` extensions.

.. program-output:: cat docgen/getting_started/buildspec-find.txt

buildtest will validate each buildspec file with the appropriate
schema type. buildspecs that pass validation will be displayed on screen.
buildtest will report all invalid buildspecs in a text file for you to review.

buildtest will cache the results in **var/buildspec-cache.json** so subsequent
runs to ``buildtest buildspec find`` will be much faster because it is read from cache.
If you make changes to buildspec you may want to rebuild the buildspec cache then
run::

  $ buildtest buildspec find --rebuild

If you want to find all buildspec files in cache run ``buildtest buildspec find --buildspec-files``

.. program-output:: cat docgen/buildspec_find_buildspecfiles.txt
     :ellipsis: 30

If you want to find root directories of buildspecs loaded in buildspec cache use the
``buildtest buildspec find --paths`` option.

::

    $ buildtest buildspec find --paths
    /Users/siddiq90/Documents/buildtest/tutorials
    /Users/siddiq90/Documents/buildtest/general_tests


buildtest will search buildspecs in :ref:`buildspecs root <buildspec_roots>` defined in your configuration,
which is a list of directory paths to search for buildspecs.
If you want to load buildspecs from a directory path, one can run specify a directory
path via ``--root`` such as ``buildtest buildspec find --root <path> --rebuild``.
buildtest will load all valid buildspecs into cache and ignore
the rest. It's important to add ``--rebuild`` if you want to regenerate buildspec cache.

Filtering buildspec
~~~~~~~~~~~~~~~~~~~

Once you have a buildspec cache, we can query the buildspec cache for certain attributes.
When you run **buildtest buildspec find** it will report all buildspecs from cache which can
be difficult to process. Therefore, we have a filter option (``--filter``) to restrict our search.
Let's take a look at the available filter fields that are acceptable with filter option.

.. program-output:: cat docgen/buildspec-filter.txt

The ``--filter`` option expects arguments in **key=value** format as follows::

    buildtest buildspec find --filter key1=value1,key2=value2,key3=value3

We can filter buildspec cache by ``tags=fail`` which will query all tests with
associated tag field in test.

.. program-output:: cat docgen/buildspec_filter_tags.txt

In addition, we can query buildspecs by schema type using ``type`` property. In this
example we query all tests by `type` property

.. program-output:: cat docgen/buildspec_filter_type.txt
   :ellipsis: 20

Finally, we can combine multiple filter fields separated by comma, in the next example
we query all buildspecs with ``tags=tutorials``, ``executor=local.sh``, and ``type=script``

.. program-output:: cat docgen/buildspec_multifield_filter.txt


Format buildspec cache
~~~~~~~~~~~~~~~~~~~~~~~

We have seen how one can filter buildspecs, but we can also configure which columns to display
in the output of **buildtest buildspec find**. By default, we show few format fields
in the output, however there are more format fields hidden from the default output.

The format fields are specified comma separated using format: ``--format <field1>,<field2>,...``.
You can see a list of all format fields by ``--helpformat`` option as shown below

.. program-output:: cat docgen/buildspec-format.txt


In the next example, we utilize ``--format`` field with ``--filter`` option to show
how format fields affect table columns. buildtest will display the table in order of
format fields specified in command line.

.. program-output:: cat docgen/buildspec_format_example.txt

buildtest makes use of python library named `tabulate <https://pypi.org/project/tabulate/>`_
to generate these tables which are found in commands line like ``buildtest buildspec find``
and ``buildtest report``.

.. _buildspec_tags:

Querying buildspec tags
~~~~~~~~~~~~~~~~~~~~~~~~

If you want to retrieve all unique tags from all buildspecs you can run
``buildtest buildspec find --tags``. This can be useful if you want to know available
tags in your buildspec cache.

.. program-output:: cat docgen/buildspec_find_tags.txt

In addition, buildtest can group tests by tags via ``buildtest buildspec find --group-by-tags``
which can be useful if you want to know which tests get executed when running ``buildtest build --tags``.
The output is grouped by tag names, followed by name of test and description.

.. program-output:: cat docgen/buildspec_find_group_by_tags.txt


.. _buildspec_executor:

Querying buildspec executor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to know all executors in your buildspec cache use the
``buildtest buildspec find --list-executors`` command. This can be useful when
you want to build by executors (``buildtest build --executor``).

.. program-output:: cat docgen/buildspec_find_executors.txt

Similar to ``--group-by-tags``, buildtest has an option to group tests by executor
using ``--group-by-executor`` option. This will show tests grouped by executor,
name of test and test description. Shown below is an example output.

.. program-output:: cat docgen/buildspec_find_group_by_executor.txt


Query Maintainers in buildspecs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``maintainers`` field can be used for identifying author for buildspec
file which can be useful if you want to find out who is responsible for the test.
You can retrieve all buildspec maintainers using ``--maintainers`` option or ``-m``
short option. The command below will show all maintainers for buildspecs in buildspec
cache

.. program-output:: cat docgen/buildspec_find_maintainers.txt


If you want to see a breakdown of maintainers by buildspec file you can use ``--maintainers-by-buildspecs``
or ``-mb`` short option. This can be useful when tracking maintainers by buildspec files.

.. program-output:: cat docgen/buildspec_find_maintainers_by_buildspecs.txt


.. _test_reports:

Test Reports (``buildtest report``)
-------------------------------------

buildtest keeps track of all test results in a JSON file which can be retrieved via
**buildtest report**. Shown below is command usage.

.. program-output:: cat docgen/buildtest_report_--help.txt

You may run ``buildtest report`` and buildtest will display all test results
with default format fields.

.. program-output:: cat docgen/report.txt
   :ellipsis: 20

Format Reports
~~~~~~~~~~~~~~~

The `buildtest report` command displays a default format fields that can be changed using the
``--format`` option. The report file (JSON) contains many more fields and we expose some of the fields
in the `--format` option. To see a list of available format fields run ``buildtest report --helpformat``.

.. program-output:: cat docgen/report-helpformat.txt


The ``--format`` field expects field name separated by comma (i.e **--format <field1>,<field2>**).
In this example we format by fields ``--format id,executor,state,returncode``. Notice, that
buildtest will display table in order of ``--format`` option.

.. program-output:: cat docgen/report-format.txt
   :ellipsis: 20

Filter Reports
~~~~~~~~~~~~~~~~

The **buildtest report** command will display all tests results, which may not be relevant when
you want to analyze specific tests. Therefore, we introduce a ``--filter`` option
to filter out tests in the output. First, lets see the available filter fields
by run ``buildtest report --helpfilter``.

.. program-output:: cat docgen/report-helpfilter.txt

The ``--filter`` option expects arguments in **key=value** format. You can
specify multiple filter delimited by comma. buildtest will treat multiple
filters as logical **AND** operation. The filter option can be used with
``--format`` field. Let's see some examples to illustrate the point.

Filter by returncode
~~~~~~~~~~~~~~~~~~~~~~

If you want to retrieve all tests with a given returncode, we can use the **returncode**
property. For instance, let's retrieve all tests with returncode of 2 by setting ``--filter returncode=2``.

.. program-output:: cat docgen/report-returncode.txt

.. Note:: buildtest automatically converts returncode to integer when matching returncode, so ``--filter returncode="2"`` will work too

Filter by test name
~~~~~~~~~~~~~~~~~~~~~

If you want to filter by test name, use the **name** attribute in filter option. Let's assume
we want to filter all tests by name ``exit1_pass`` which can be done by
setting ``--filter name=exit1_pass`` as shown below

.. program-output:: cat docgen/report-filter-name.txt

Filter by buildspec
~~~~~~~~~~~~~~~~~~~~~

Likewise, we can filter results by buildspec file using **buildspec** attribute via
``--filter buildspec=<file>``. The **buildspec** attribute must resolve to a file path which can be
relative or absolute path. buildtest will resolve path (absolute path) and find the appropriate
tests that belong to the buildspec file. If file doesn't exist or is not found in cache it will raise an error.

.. program-output:: cat docgen/report-filter-buildspec.txt

Filter by test state
~~~~~~~~~~~~~~~~~~~~~

If you want to filter results by test state, use the **state** property. This can be
useful if you want to know all pass or failed tests. The state property expects
value of ``[PASS|FAIL]`` since these are the two recorded test states marked by buildtest.

We can also pass multiple filter fields for instance if we want to find all **FAIL**
tests for executor **local.sh** we can do the following.

.. program-output:: cat docgen/report-multifilter.txt

Filter Exception Cases
~~~~~~~~~~~~~~~~~~~~~~~~

The ``returncode`` filter field expects an integer value, so if you try a non-integer
returncode you will get the following message::

    $ buildtest report --filter returncode=1.5
    Traceback (most recent call last):
      File "/Users/siddiq90/Documents/buildtest/bin/buildtest", line 17, in <module>
        buildtest.main.main()
      File "/Users/siddiq90/Documents/buildtest/buildtest/main.py", line 45, in main
        args.func(args)
      File "/Users/siddiq90/Documents/buildtest/buildtest/menu/report.py", line 128, in func_report
        raise BuildTestError(f"Invalid returncode:{filter_args[key]} must be an integer")
    buildtest.exceptions.BuildTestError: 'Invalid returncode:1.5 must be an integer'

The ``state`` filter field expects value of ``PASS`` or ``FAIL`` so if you specify an
invalid state you will get an error as follows::

    $ buildtest report --filter state=UNKNOWN
    filter argument 'state' must be 'PASS' or 'FAIL' got value UNKNOWN

The ``buildspec`` field expects a valid file path, it can be an absolute or relative
path, buildtest will resolve absolute path and check if file exist and is in the report
file. If it's an invalid file we get an error such as::

    $ buildtest report --filter buildspec=/path/to/invalid.yml
    Invalid File Path for filter field 'buildspec': /path/to/invalid.yml

You may have a valid filepath for buildspec filter field such as
``tutorials/invalid_executor.yml``, but there is no record in the report cache
because this test can't be run. In this case you will get the following message::

    $ buildtest report --filter buildspec=tutorials/invalid_executor.yml
    buildspec file: /Users/siddiq90/Documents/buildtest/tutorials/invalid_executor.yml not found in cache

Find Latest or Oldest test
~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can search for oldest or latest test for any given test. This can be useful if you
want to see first or last test run. If you want to retrieve the oldest
test you can use ``--oldest`` option. buildtest will append tests, therefore last
record in dictionary will be latest record, similarly first record is the oldest record.

Let's take a look at this example, we filter by test name ``hello_f`` which retrieves
three entries. Now let's filter by oldest record by specifying **--oldest** option
and it will retrieve the first record which is test id **349f3ada**.

.. code-block::

   $ buildtest report --filter name=hello_f --format name,id,starttime
    +---------+----------+---------------------+
    | name    | id       | starttime           |
    +=========+==========+=====================+
    | hello_f | 349f3ada | 2021/02/11 18:13:08 |
    +---------+----------+---------------------+
    | hello_f | ecd4a3f2 | 2021/02/11 18:13:18 |
    +---------+----------+---------------------+
    | hello_f | 5c87978b | 2021/02/11 18:13:33 |
    +---------+----------+---------------------+

    $ buildtest report --filter name=hello_f --format name,id,starttime --oldest
    +---------+----------+---------------------+
    | name    | id       | starttime           |
    +=========+==========+=====================+
    | hello_f | 349f3ada | 2021/02/11 18:13:08 |
    +---------+----------+---------------------+


If you want to retrieve the latest test result you can use ``--latest`` option which
will retrieve the last record, in the same example we will retrieve test id `5c87978b`.


.. code-block::

    $ buildtest report --filter name=hello_f --format name,id,starttime --latest
    +---------+----------+---------------------+
    | name    | id       | starttime           |
    +=========+==========+=====================+
    | hello_f | 5c87978b | 2021/02/11 18:13:33 |
    +---------+----------+---------------------+

You may combine **--oldest** and **--latest** options in same command, in this case
buildtest will retrieve the first and last record of every test.

.. code-block::

    $ buildtest report --format name,id,starttime --oldest --latest | more
    +------------------------------+----------+---------------------+
    | name                         | id       | starttime           |
    +==============================+==========+=====================+
    | variables_bash               | 750f48bc | 2021/02/11 18:13:03 |
    +------------------------------+----------+---------------------+
    | variables_bash               | 1bdfd403 | 2021/02/11 18:13:32 |
    +------------------------------+----------+---------------------+
    | ulimit_filelock_unlimited    | b7b852e4 | 2021/02/11 18:13:03 |
    +------------------------------+----------+---------------------+
    | ulimit_filelock_unlimited    | 56345a43 | 2021/02/11 18:13:18 |
    +------------------------------+----------+---------------------+

Test Inspection
-----------------

buildtest provides an interface via ``buildtest inspect`` to query test details once
test is recorded in ``var/report.json``. The command usage is the following.

.. program-output:: cat docgen/buildtest_inspect_--help.txt

The ``buildtest inspect`` expects a **unique** test id this can be
retrieve using the ``full_id`` format field if you are not sure::

  $ buildtest report --format name,full_id

For example, let's assume we have the following tests in our report::

    $ buildtest report --format name,full_id
    +-------------------------+--------------------------------------+
    | name                    | full_id                              |
    +=========================+======================================+
    | bash_login_shebang      | eb6e26b2-938b-4913-8b98-e21528c82778 |
    +-------------------------+--------------------------------------+
    | bash_login_shebang      | d7937a9a-d3fb-4d3f-95e1-465488757820 |
    +-------------------------+--------------------------------------+
    | bash_login_shebang      | dea6c6fd-b9a6-4b07-a3fc-b483d02d7ff9 |
    +-------------------------+--------------------------------------+
    | bash_nonlogin_shebang   | bbf94b94-949d-4f97-987a-9a93309f1dc2 |
    +-------------------------+--------------------------------------+
    | bash_nonlogin_shebang   | 7ca9db2f-1e2b-4739-b9a2-71c8cc00249e |
    +-------------------------+--------------------------------------+
    | bash_nonlogin_shebang   | 4c5caf85-6ba0-4ca0-90b0-c769a2fcf501 |
    +-------------------------+--------------------------------------+
    | root_disk_usage         | e78071ef-6444-4228-b7f9-b4eb39071fdd |
    +-------------------------+--------------------------------------+
    | ulimit_filelock         | c6294cfa-c559-493b-b44f-b17b54ec276d |
    +-------------------------+--------------------------------------+
    | ulimit_cputime          | aa5530e2-be09-4d49-b8c0-0e818f855a40 |
    +-------------------------+--------------------------------------+
    | ulimit_stacksize        | 3591925d-7dfa-4bc7-a3b1-fb9dfadf956e |
    +-------------------------+--------------------------------------+
    | ulimit_vmsize           | 4a01f26b-9c8a-4870-8e33-51923c8c46ad |
    +-------------------------+--------------------------------------+
    | ulimit_filedescriptor   | 565b85ac-e51f-46f9-8c6f-c2899a370609 |
    +-------------------------+--------------------------------------+
    | ulimit_max_user_process | 0486c11c-5733-4d8e-822e-c0adddbb2af7 |
    +-------------------------+--------------------------------------+
    | systemd_default_target  | 7cfc9057-6338-403c-a7af-b1301d04d817 |
    +-------------------------+--------------------------------------+

Let's assume we are interested in viewing test ``bash_login_shebang``, since we
have multiple instance for same test we must specify a unique id. In example below
we query the the test id **eb6e26b2-938b-4913-8b98-e21528c82778**::

    $ buildtest inspect eb6e26b2-938b-4913-8b98-e21528c82778
    {
      "id": "eb6e26b2",
      "full_id": "eb6e26b2-938b-4913-8b98-e21528c82778",
      "testroot": "/Users/siddiq90/Documents/buildtest/var/tests/local.bash/shebang/bash_login_shebang/0",
      "testpath": "/Users/siddiq90/Documents/buildtest/var/tests/local.bash/shebang/bash_login_shebang/0/stage/generate.sh",
      "command": "/Users/siddiq90/Documents/buildtest/var/tests/local.bash/shebang/bash_login_shebang/0/stage/generate.sh",
      "outfile": "/Users/siddiq90/Documents/buildtest/var/tests/local.bash/shebang/bash_login_shebang/0/run/bash_login_shebang.out",
      "errfile": "/Users/siddiq90/Documents/buildtest/var/tests/local.bash/shebang/bash_login_shebang/0/run/bash_login_shebang.err",
      "schemafile": "script-v1.0.schema.json",
      "executor": "local.bash",
      "tags": "tutorials",
      "starttime": "2020/10/21 16:27:18",
      "endtime": "2020/10/21 16:27:18",
      "runtime": 0.26172968399999996,
      "state": "PASS",
      "returncode": 0
    }



    Output File
    ______________________________
    Login Shell




    Error File
    ______________________________




    Test Content
    ______________________________
    #!/bin/bash -l
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/before_script.sh
    shopt -q login_shell && echo 'Login Shell' || echo 'Not Login Shell'
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/after_script.sh



    buildspec:  /Users/siddiq90/Documents/buildtest/tutorials/shebang.yml
    ______________________________
    version: "1.0"
    buildspecs:
      bash_login_shebang:
        type: script
        executor: local.bash
        shebang: "#!/bin/bash -l"
        description: customize shebang line with bash login shell
        tags: tutorials
        run: shopt -q login_shell && echo 'Login Shell' || echo 'Not Login Shell'
        status:
          regex:
            exp: "^Login Shell$"
            stream: stdout

      bash_nonlogin_shebang:
        type: script
        executor: local.bash
        shebang: "#!/bin/bash"
        description: customize shebang line with default bash (nonlogin) shell
        tags: tutorials
        run: shopt -q login_shell && echo 'Login Shell' || echo 'Not Login Shell'
        status:
          regex:
            exp: "^Not Login Shell$"
            stream: stdout



buildtest will present the test record from JSON record including contents of
output file, error file, testscript and buildspec file.

User can can specify first few characters of the id and buildtest will detect if
its a unique test id. If buildtest discovers more than one test id, then buildtest
will report all the ids where there is a conflict. In example below we find
two tests with id **7c**::

    $ buildtest inspect 7c
    Detected 2 test records, please specify a unique test id
    7ca9db2f-1e2b-4739-b9a2-71c8cc00249e
    7cfc9057-6338-403c-a7af-b1301d04d817

.. note:: This feature is in development and may change in future

.. _buildtest_schemas:

buildtest schemas
------------------

The ``buildtest schema`` command can show you list of available schemas just run
the command with no options and it will show all the json schemas supported by buildtest.

.. program-output:: cat docgen/schemas/avail-schemas.txt

Shown below is the command usage of ``buildtest schema``

.. program-output:: cat docgen/buildtest_schema_--help.txt

The json schemas are hosted on the web at https://buildtesters.github.io/buildtest/.
buildtest provides a means to display the json schema from the buildtest interface.

To select a JSON schema use the ``--name`` option to select a schema, for example
to view a JSON Schema for **script-v1.0.schema.json** run the following::

  $ buildtest schema --name script-v1.0.schema.json --json

Similarly, if you want to view example buildspecs for a schema use the ``--example``
option with a schema. For example to view all example schemas for
**compiler-v1.0.schema.json** run the following::

  $ buildtest schema --name compiler-v1.0.schema.json --example

Debug Mode
------------

buildtest can stream logs to ``stdout`` stream for debugging. You can use ``buildtest -d <DEBUGLEVEL>``
or long option ``--debug`` with any buildtest commands. The DEBUGLEVEL are the following:

- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

buildtest is using `logging.setLevel <https://docs.python.org/3/library/logging.html#logging.Logger.setLevel>`_
to control log level. The content is logged in file **buildtest.log** in your current
directory with default log level of ``DEBUG``. If you want to get all logs use
``-d DEBUG`` with your buildtest command::

    buildtest -d DEBUG <command>

The debug mode can be useful when troubleshooting builds, in this example we
set debug level to ``DEBUG`` for an invalid buildspec.

.. program-output:: cat docgen/getting_started/debug-mode.txt

Accessing buildtest documentation
----------------------------------

We provide two command line options to access main documentation and schema docs. This
will open a browser on your machine.

To access `buildtest docs <https://buildtest.readthedocs.io/>`_ you can run::

  $ buildtest docs

To access `schema docs <https://buildtesters.github.io/buildtest>`_ you can run::

  $ buildtest schemadocs
