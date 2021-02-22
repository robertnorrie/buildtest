.. _configuring_buildtest:

Configuring buildtest
======================

The buildtest configuration file is used for configuring buildtest.
This is defined by JSON schemafile named `settings.schema.json <https://raw.githubusercontent.com/buildtesters/buildtest/devel/buildtest/schemas/settings.schema.json>`_.
For more details on all properties see `Settings Schema Documentation <https://buildtesters.github.io/buildtest/pages/schemadocs/settings.html>`_.


Default Configuration
-----------------------

The default buildtest configuration  is located at `buildtest/settings/config.yml <https://raw.githubusercontent.com/buildtesters/buildtest/devel/buildtest/settings/config.yml>`_
relative to root of repo. User may override the default configuration by creating
their own buildtest configuration at ``$HOME/.buildtest/config.yml`` and buildtest
will read the user configuration instead.

Shown below is the default configuration provided by buildtest.

.. program-output:: cat ../buildtest/settings/config.yml

.. _configuring_executors:

What is an executor?
----------------------

An executor is responsible for running the test and capture output/error file and
return code. An executor can be local executor which runs tests on local machine or
batch executor that can be modelled as partition/queue. A batch executor is
responsible for **dispatching** job, then **poll** job until its finish, and
**gather** job metrics from scheduler.

Executor Declaration
--------------------

`executors` is a JSON `object`, the structure looks as follows::

  executors:
    local:
      <local1>:
      <local2>:
      <local3>:
    slurm:
      <slurm1>:
      <slurm2>:
      <slurm3>:
    lsf:
      <lsf1>:
      <lsf2>:
      <lsf3>:

The **LocalExecutors** are defined in section `local` where each executor must be
unique name::

  executors:
    local:

The *LocalExecutors* can be ``bash``, ``sh``, ``csh``, ``tcsh`` and ``python`` shell and they are
referenced in buildspec using ``executor`` field as follows::

    executor: local.bash

The executor is referenced in buildspec in the format: ``<type>.<name>`` where
**type** is **local**, **slurm**, **lsf**, **cobalt** defined in the **executors** section
and **name** is the executor name. In example above `local.bash` refers to the LocalExecutor
using bash shell. Similarly, **SlurmExecutors** and **LSFExecutors** are defined
in similar structure.

Shown below is the declaration of a bash executor named `bash` that is referenced
in buildspec as ``executor: local.bash``::

    executors:
      local:
        bash:
          shell: bash

The local executors requires the ``shell`` key which takes the pattern
``"^(/bin/bash|/bin/sh|/bin/csh|/bin/tcsh|/bin/zsh|sh|bash|csh|tcsh|zsh|python).*"``.
Any buildspec that references ``local.bash`` executor will submit job using ``bash`` shell.

You can pass options to shell which will get passed into each job submission.
For instance if you want all bash scripts to run in login shell you can specify ``bash --login``.::

    executors:
      local:
        login_bash:
          shell: bash --login

Then you can reference this executor as ``executor: local.login_bash`` and your
tests will be submitted via ``bash --login /path/to/test.sh``.

.. _slurm_executors:

buildtest configuration for Cori @ NERSC
------------------------------------------

Let's take a look at Cori buildtest configuration::

    editor: vi
    buildspec_roots:
    - $HOME/buildtest-cori
    moduletool: environment-modules
    executors:
      defaults:
        pollinterval: 10
        launcher: sbatch
        max_pend_time: 90
        account: nstaff
      local:
        bash:
          description: submit jobs on local machine using bash shell
          shell: bash
        sh:
          description: submit jobs on local machine using sh shell
          shell: sh
        csh:
          description: submit jobs on local machine using csh shell
          shell: csh
        python:
          description: submit jobs on local machine using python shell
          shell: python
        e4s:
          description: E4S testsuite locally
          shell: bash
          before_script: |
            source /global/common/software/spackecp/luke-wyatt-testing/spack/share/spack/setup-env.sh
            cd $SCRATCH/testsuite source setup.sh

      slurm:
        debug:
          description: jobs for debug qos
          qos: debug
          cluster: cori
          max_pend_time: 500
        shared:
          description: jobs for shared qos
          qos: shared
          max_pend_time: 10
        bigmem:
          description: bigmem jobs
          cluster: escori
          qos: bigmem
          max_pend_time: 300
        xfer:
          description: xfer qos jobs
          qos: xfer
          cluster: escori
        gpu:
          description: submit jobs to GPU partition
          options:
          - -C gpu
          cluster: escori
          max_pend_time: 300
        premium:
          description: submit jobs to premium queue
          qos: premium
        e4s:
          description: E4S runner
          cluster: cori
          max_pend_time: 20000
          options:
          - -q regular
          - -C knl
          - -t 10
          - -n 4
          before_script: |
            source /global/common/software/spackecp/luke-wyatt-testing/spack/share/spack/setup-env.sh
            cd $SCRATCH/testsuite source setup.sh

    compilers:
      find:
        gcc: "^(gcc|PrgEnv-gnu)"
        cray: "^(PrgEnv-cray)"
        intel: "^(intel|PrgEnv-intel)"
        pgi: "^(pgi)"
      compiler:
        gcc:
          builtin_gcc:
            cc: /usr/bin/gcc
            cxx: /usr/bin/g++
            fc: /usr/bin/gfortran

In this setting, we define the following executors

- LocalExecutors: ``local.bash``, ``local.sh``, ``local.csh``, ``local.python``, ``local.e4s``
- SlurmExecutors: ``slurm.debug``, ``slurm.shared``, ``slurm.bigmem``, ``slurm.xfer``, ``slurm.gpu``, ``slurm.premium``, ``slurm.e4s``


We introduce section ``defaults`` which defines configuration for all executors
as follows::

      defaults:
        pollinterval: 10
        launcher: sbatch
        max_pend_time: 90
        account: nstaff

The `launcher` field is applicable for batch executors in this
case, ``launcher: sbatch`` inherits **sbatch** as the job launcher for all executors.
The ``pollinterval`` field is used  to poll jobs at set interval in seconds
when job is active in queue. The ``max_pend_time`` is **maximum** time job can be pending
within an executor, if it exceeds the limit buildtest will cancel the job. The
`pollinterval`, `launcher` and `max_pend_time` have no effect on local executors.
The ``account: nstaff`` will instruct buildtest to charge all jobs to account
``nstaff`` from Slurm Executors. The ``account`` option can be set in ``defaults``
global to all executors or set per executor instance which overrides the default value.

At Cori, jobs are submitted via qos instead of partition so we model a slurm executor
named by qos. The ``qos`` field instructs which Slurm QOS to use when submitting job.
The ``description`` key is a brief description of the executor only served for
documentation purpose. The ``cluster`` field specifies which slurm cluster to use
(i.e ``sbatch --clusters=<string>``). In-order to use ``bigmem``, ``xfer``,
or ``gpu`` qos at Cori, we need to specify **escori** cluster (i.e
``sbatch --clusters=escori``).

buildtest will detect slurm configuration and check qos, partition, cluster
match with buildtest specification. In addition, buildtest supports multi-cluster
job submission and monitoring from remote cluster. This means if you specify
``cluster`` field buildtest will poll jobs using `sacct` with the
cluster name as follows: ``sacct -M <cluster>``.

The ``options`` field is use to specify any additional options to launcher (``sbatch``)
on command line. For ``slurm.gpu`` executor, we use the ``options: -C gpu``
in order to submit to Cori GPU cluster which requires ``sbatch -M escori -C gpu``.
Any additional **#SBATCH** options are
defined in buildspec for more details see :ref:`batch scheduler support <batch_support>`

The ``max_pend_time`` option can be overridden per executor level for example the
section below overrides the default to 300 seconds::

        bigmem:
          description: bigmem jobs
          cluster: escori
          qos: bigmem
          max_pend_time: 300

The ``max_pend_time`` is used to cancel job only if job is pending in queue, it has
no impact if job is running. buildtest starts a timer at job submission and every poll interval (``pollinterval`` field)
checks if job has exceeded **max_pend_time** only if job is in **PENDING** (SLURM)
or **PEND** (LSF) state. If job pendtime exceeds `max_pend_time` limit, buildtest will
cancel job using ``scancel`` or ``bkill`` depending on the scheduler. Buildtest
will remove cancelled jobs from poll queue, in addition cancelled jobs won't be
reported in test report.

.. _buildspec_roots:

buildspec roots
-----------------

buildtest can discover buildspec using ``buildspec_roots`` keyword. This field is a list
of directory paths to search for buildspecs. For example we clone the repo
https://github.com/buildtesters/buildtest-cori at **$HOME/buildtest-cori** and assign
this to **buildspec_roots** as follows::

    buildspec_roots:
      - $HOME/buildtest-cori

This field is used with the ``buildtest buildspec find`` command. If you rebuild
your buildspec cache use ``--rebuild`` option it will detect all buildspecs in defined
in all directories specified by **buildspec_roots**. buildtest will recursively
find all **.yml** extension and validate each buildspec with appropriate schema.
By default buildtest will add the ``$BUILDTEST_ROOT/tutorials`` and ``$BUILDTEST_ROOT/general_tests``
to search path, where $BUILDTEST_ROOT is root of repo.

The `load_default_buildspecs` property can be used to control if you want buildtest to
load default buildspecs into cache when you run ``buildtest buildspec find`` or with
``--rebuild`` option. It can be useful to set ``load_default_buildspecs: False`` if you
only care about running your facility tests. .

Configuring Module Tool
------------------------

You should configure the ``moduletool`` property to the module-system installed
at your site. Valid options are the following::

    # environment-modules
    moduletool: environment-modules

    # for lmod
    moduletool: lmod

    # specify N/A if you don't have modules
    moduletool: N/A

If your site has Lmod and you set ``moduletool: lmod``, we will make use of
`Lmodule API <https://lmodule.readthedocs.io/en/latest/>`_ to test modules.

Configuring where to write tests
---------------------------------

The default location where tests are written is **$BUILDTEST_ROOT/var/tests** where
$BUILDTEST_ROOT is the root of buildtest repo. You may specify ``testdir`` in your
configuration to instruct where tests can be written. For instance, if
you want to write tests in **/tmp** you can set the following::

    testdir: /tmp

Alternately, one can specify test directory via ``buildtest build --testdir <path>`` which
has highest precedence and overrides configuration and default value.

Configuring log path
----------------------

You can configure where buildtest will write logs using ``logdir`` property. For
example, in example below buildtest will write log files ``$HOME/Documents/buildtest/var/logs``.
buildtest will resolve variable expansion to get real path on filesystem.


::

    # location of log directory
    logdir: $HOME/Documents/buildtest/var/logs


``logdir`` is not required in configuration, if it's not specified buildtest will write logs
based on `tempfile <https://docs.python.org/3/library/tempfile.html>`_ library which may vary
based on platform (Linux, Mac).

For instance, on Mac the directory path may be something as follows::

    /var/folders/1m/_jjv09h17k37mkktwnmbkmj0002t_q/T/buildtest_dy_xu1eb.log

The buildtest logs will start with **buildtest_** followed by random identifier with
a **.log** extension.

before_script and after_script for executors
---------------------------------------------

Often times, you may want to run a set of commands before or after tests for more than
one test. For this reason, we support ``before_script`` and ``after_script`` section
per executor which is of string type where you can specify multi-line commands.

This can be demonstrated with an executor name **local.e4s** responsible for
building `E4S Testsuite <https://github.com/E4S-Project/testsuite>`_::

    e4s:
      description: "E4S testsuite locally"
      shell: bash
      before_script: |
        cd $SCRATCH
        git clone https://github.com/E4S-Project/testsuite.git
        cd testsuite
        source /global/common/software/spackecp/luke-wyatt-testing/spack/share/spack/setup-env.sh
        source setup.sh

The `e4s` executor attempts to clone E4S Testsuite in $SCRATCH and activate
a spack environment and run the initialize script ``source setup.sh``. buildtest
will write a ``before_script.sh`` and ``after_script.sh`` for every executor.
This can be found in ``var/executors`` directory as shown below::

    $ tree var/executors/
    var/executors/
    |-- local.bash
    |   |-- after_script.sh
    |   `-- before_script.sh
    |-- local.e4s
    |   |-- after_script.sh
    |   `-- before_script.sh
    |-- local.python
    |   |-- after_script.sh
    |   `-- before_script.sh
    |-- local.sh
    |   |-- after_script.sh
    |   `-- before_script.sh


    4 directories, 8 files

The ``before_script`` and ``after_script`` field is available for all executors and
if its not specified the file will be empty. Every test will source the before
and after script for the given executor.

Compiler Declaration
--------------------

buildtest provides a mechanism to declare compilers in your configuration file, this
is defined in ``compilers`` top-level section. Shown below is a declaration of builtin
gcc provided by default::

    compilers:
      compiler:
        gcc:
          builtin_gcc:
            cc: /usr/bin/gcc
            cxx: /usr/bin/g++
            fc: /usr/bin/gfortran

The compiler declaration is defined in section ``compiler`` followed by name
of compiler in this case ``gcc``. In the gcc section one can define all gnu compilers,
which includes the name of the compiler in this example we call ``builtin_gcc`` as
system compiler that defines C, C++ and Fortran compilers using ``cc``, ``cxx`` and
``fc``.

One can retrieve all compilers using ``buildtest config compilers``, there are few
options for this command.

.. program-output:: cat docgen/buildtest_config_compilers_--help.txt

buildtest can represent compiler output in JSON, YAML or list using the ``--json``,
``--yaml``, and ``--list`` option. Depending on your preference one can view
compiler section with any of these options. Shown below is an example output with
these options::

    $ buildtest config compilers --json
    {
      "gcc": {
        "builtin_gcc": {
          "cc": "/usr/bin/gcc",
          "cxx": "/usr/bin/g++",
          "fc": "/usr/bin/gfortran"
        }
      }
    }

    $ buildtest config compilers --yaml
    gcc:
      builtin_gcc:
        cc: /usr/bin/gcc
        cxx: /usr/bin/g++
        fc: /usr/bin/gfortran

    $ buildtest config compilers --list
    builtin_gcc

Detect Compilers (Experimental Feature)
----------------------------------------

buildtest can detect compilers based on modulefiles and generate compiler section
that way you don't have to specify each compiler manually.
This can be done via ``buildtest config compilers find`` command. Buildtest expects
a key/value mapping when searching compiler names and regular expression (``re.match``)
is used for discovering compiler modules.


This can be demonstrated, by defining search pattern in the ``find`` section
that expects a dictionary of key/value mapping between compiler names and their module names.

In example, below we define a pattern for gcc modules as ``^(gcc)`` which will
find all modules that start with name `gcc`.

::

    compilers:
      find:
        gcc: "^(gcc)"
      compiler:
        gcc:
          builtin:
            cc: /usr/bin/gcc
            cxx: /usr/bin/g++
            fc: /usr/bin/gfortran


In this system, we have two gcc modules installed via `spack <https://spack.readthedocs.io/en/latest/>`_
package manager, we will attempt to add both modules as compiler instance in buildtest.

::

    $ module -t av gcc
    /Users/siddiq90/projects/spack/share/spack/lmod/darwin-catalina-x86_64/Core:
    gcc/9.3.0-n7p74fd
    gcc/10.2.0-37fmsw7


Next we run ``buildtest config compilers find`` which will search all modules based on
regular expression and add compilers in their respective group. In this example, buildtest
automatically add ``gcc/9.2.0-n7p74fd`` and ```gcc/10.2.0-37fmsw7`` modules as compiler
instance. Depending on the compiler group, buildtest will apply the compiler wrapper
``cc``, ``cxx``, ``fc`` however these can be updated manually. The module section
is generated with the module to load. One can further tweak the module behavior
along with purging or swap modules.

::

    $ buildtest config compilers find
    MODULEPATH: /Users/siddiq90/projects/spack/share/spack/lmod/darwin-catalina-x86_64/Core:/usr/local/Cellar/lmod/8.4.12/modulefiles/Darwin:/usr/local/Cellar/lmod/8.4.12/modulefiles/Core
    Configuration File: /Users/siddiq90/.buildtest/config.yml
    ________________________________________________________________________________
    moduletool: lmod
    load_default_buildspecs: true
    executors:
      local:
        bash:
          description: submit jobs on local machine using bash shell
          shell: bash
        sh:
          description: submit jobs on local machine using sh shell
          shell: sh
        csh:
          description: submit jobs on local machine using csh shell
          shell: csh
        python:
          description: submit jobs on local machine using python shell
          shell: python
    compilers:
      find:
        gcc: ^(gcc)
        pgi: ^(pgi)
      compiler:
        gcc:
          builtin_gcc:
            cc: /usr/bin/gcc
            cxx: /usr/bin/g++
            fc: /usr/local/bin/gfortran
          gcc/9.3.0-n7p74fd:
            cc: gcc
            cxx: g++
            fc: gfortran
            module:
              load:
              - gcc/9.3.0-n7p74fd
              purge: false
          gcc/10.2.0-37fmsw7:
            cc: gcc
            cxx: g++
            fc: gfortran
            module:
              load:
              - gcc/10.2.0-37fmsw7
              purge: false

    ________________________________________________________________________________
    Updating settings file:  /Users/siddiq90/.buildtest/config.yml


This feature relies on module system (Lmod, environment-modules) to search modulefiles
and one must specify **moduletool** property to indicate how buildtest will search modules.
If ``moduletool: lmod`` is set, buildtest will rely on Lmod spider using `Lmodule  <http://lmodule.readthedocs.io/>`_
API to detect and test all modules. If ``moduletool: environment-modules`` is set, buildtest
will retrieve modules using output of ``module -t av``.


buildtest configuration for Ascent @ OLCF
------------------------------------------

`Ascent <https://docs.olcf.ornl.gov/systems/ascent_user_guide.html>`_ is a training
system for Summit at OLCF, which is using a IBM Load Sharing
Facility (LSF) as their batch scheduler. Ascent has two
queues **batch** and **test**. To declare LSF executors we define them under ``lsf``
section within the ``executors`` section.

The default launcher is `bsub` which can be defined under ``defaults``. The
``pollinterval`` will poll LSF jobs every 10 seconds using ``bjobs``. The
``pollinterval`` accepts a range between **10 - 300** seconds as defined in
schema. In order to avoid polling scheduler excessively pick a number that is best
suitable for your site::

    moduletool: lmod
    load_default_buildspecs: true
    executors:
      defaults:
        launcher: bsub
        pollinterval: 10
        max_pend_time: 45

      local:
        bash:
          description: submit jobs on local machine using bash shell
          shell: bash

        sh:
          description: submit jobs on local machine using sh shell
          shell: sh

        csh:
          description: submit jobs on local machine using csh shell
          shell: csh

        python:
          description: submit jobs on local machine using python shell
          shell: python
      lsf:
        batch:
          queue: batch
          description: Submit job to batch queue

        test:
          queue: test
          description: Submit job to test queue


buildtest configuration for JLSE @ ANL
---------------------------------------

`Joint Laboratory for System Evaluation (JLSE) <https://www.jlse.anl.gov/>`_ provides
a testbed of emerging HPC systems, the default scheduler is Cobalt, this is
defined in the ``cobalt`` section defined in the executor field.

We set default launcher to qsub defined with ``launcher: qsub``. This is inherited
for all batch executors. In each cobalt executor the ``queue`` property will specify
the queue name to submit job, for instance the executor ``yarrow`` with ``queue: yarrow``
will submit job using ``qsub -q yarrow`` when using this executor.

::

    buildspec_roots:
      - $HOME/jlse_tests
    executors:
      defaults:
         launcher: qsub
         pollinterval: 10
         max_pend_time: 10

      local:
        bash:
          description: submit jobs on local machine using bash shell
          shell: bash

        sh:
          description: submit jobs on local machine using sh shell
          shell: sh

        csh:
          description: submit jobs on local machine using csh shell
          shell: csh

        python:
          description: submit jobs on local machine using python shell
          shell: python

      cobalt:
        yarrow:
          queue: yarrow

        yarrow_debug:
          queue: yarrow_debug

        iris:
          queue: iris

        iris_debug:
          queue: iris_debug

CLI to buildtest configuration
-----------------------------------------------

The ``buildtest config`` command provides access to buildtest configuration, shown
below is the command usage.


.. program-output:: cat docgen/buildtest_config_--help.txt


View buildtest configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to view buildtest configuration you can run the following

.. program-output:: cat docgen/config-view.txt

.. Note:: ``buildtest config view`` will display contents of user buildtest settings ``~/.buildtest/config.yml`` if found, otherwise it will display the default configuration


Validate buildtest configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To check if your buildtest settings is valid, run ``buildtest config validate``.
This will validate your configuration with the schema **settings.schema.json**.
The output will be the following.

.. program-output:: cat docgen/config-validate.txt

.. Note:: If you defined a user setting (``~/.buildtest/config.yml``) buildtest will validate this file instead of default one.

If there is an error during validation, the output from **jsonschema.exceptions.ValidationError**
will be displayed in terminal. For example the error below indicates that
``moduletool`` property was expecting one of the values
[``environment-modules``, ``lmod``, ``N/A``] but it recieved a value of ``none``::

    $ buildtest config validate
    Traceback (most recent call last):
      File "/Users/siddiq90/Documents/buildtest/bin/buildtest", line 17, in <module>
        buildtest.main.main()
      File "/Users/siddiq90/Documents/buildtest/buildtest/main.py", line 39, in main
        buildtest_configuration = check_settings(settings_file, retrieve_settings=True)
      File "/Users/siddiq90/Documents/buildtest/buildtest/config.py", line 41, in check_settings
        validate(instance=user_schema, schema=config_schema)
      File "/Users/siddiq90/.local/share/virtualenvs/buildtest-1gHVG2Pd/lib/python3.7/site-packages/jsonschema/validators.py", line 934, in validate
        raise error
    jsonschema.exceptions.ValidationError: 'none' is not one of ['environment-modules', 'lmod', 'N/A']

    Failed validating 'enum' in schema['properties']['moduletool']:
        {'description': 'Specify modules tool used for interacting with '
                        '``module`` command. ',
         'enum': ['environment-modules', 'lmod', 'N/A'],
         'type': 'string'}

    On instance['moduletool']:
        'none'

Configuration Summary
~~~~~~~~~~~~~~~~~~~~~~

You can get a summary of buildtest using ``buildtest config summary``, this will
display information from several sources into one single command along.

.. program-output:: cat docgen/config-summary.txt


Example Configurations
-------------------------

buildtest provides a few example configurations for configuring buildtest this
can be retrieved by running ``buildtest schema -n settings.schema.json --examples``
or short option (``-e``), which will validate each example with schema file
``settings.schema.json``.

.. program-output:: cat docgen/schemas/settings-examples.txt

If you want to retrieve full json schema file for buildtest configuration you can
run ``buildtest schema -n settings.schema.json --json`` or short option ``-j``.
