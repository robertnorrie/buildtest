import json
import os
from jsonschema.exceptions import ValidationError
from buildtest.buildsystem.parser import BuildspecParser
from buildtest.config import check_settings
from buildtest.schemas.utils import here
from buildtest.schemas.defaults import schema_table
from buildtest.utils.file import walk_tree, read_file


def func_schema(args):
    """This method implements command ``buildtest schema`` which shows a list
       of schemas, their json content and list of schema examples. The input
       ``args`` is an instance of argparse class that contains
       user selection via command line. This method can do the following

       ``buildtest schema`` - Show all schema names
       ``buildtest schema --name <NAME> -j ``. View json content of a specified schema
       ``buildtest schema --name <NAME> -e``. Show schema examples
       Parameters:

       :param args: instance of argparse class
       :type args: <class 'argparse.Namespace'>
       :result: output of json schema on console
    """

    # the default behavior when "buildtest schema" is executed is to show list of all
    # schemas
    if not args.json and not args.example:
        for schema in schema_table["names"]:
            print(schema)
        return

    # -n option is required when using -j or -e option
    if not args.name:
        raise SystemExit(
            "Please specify a schema name with -n option when using -j or -e option"
        )

    if args.json:
        print(json.dumps(schema_table[args.name]["recipe"], indent=2))
        return

    # There are no examples for definitions schema
    if args.name == "definitions.schema.json" and args.example:
        raise SystemExit("There are no examples for definitions.schema.json")

    examples = os.path.join(here, "examples", args.name)

    # get all examples for specified schema. We validate all examples and
    # and print content of all examples. If there is an error during validation
    # we show the error message.
    if args.example:
        schema_examples = walk_tree(examples, ".yml")
        for example in schema_examples:
            valid_state = True
            err_msg = None
            # for settings.schema.json we validate each test by running check_settings
            if args.name == "settings.schema.json":
                try:
                    check_settings(example, executor_check=False)
                except ValidationError as err:
                    valid_state = "FAIL"
                    err_msg = err
            # the rest of schemas are validated using BuildspecParser
            else:
                try:
                    BuildspecParser(example)
                except (SystemExit, ValidationError) as err:
                    valid_state = "FAIL"
                    err_msg = err

            content = read_file(example)
            print("\n\n")
            print(f"File: {example}")
            print(f"Valid State: {valid_state}")
            print("{:_<80}".format(""))
            print("\n")
            print(content)

            if err_msg:
                print("{:_<40} Validation Error {:_<40}".format("", ""))
                print(err_msg)