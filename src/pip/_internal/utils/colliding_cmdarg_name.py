import json
from pip._internal.exceptions import CollidingNameError, BadCommand
import re
import pathlib

from pip._vendor import requests
import sys
# from pip._internal.cli.main_parser import parse_command
from pip._internal.cli.req_command import IndexGroupCommand

from pathlib import Path
from pip._internal.utils.misc import write_output

suspiscious_packages = []
package_name = ""
suggested_package = ""
command = sys.argv[1]
mal_type = ""
yes_no = ""

def is_colliding(args):
    global package_name
    try:
        to_check = args[0].req.name
        package_name = args[0].req.name
    except (AttributeError, IndexError):
        to_check = args
    global suggested_package
    global mal_type
    dir_path = str(pathlib.Path(__file__).parent.absolute())
    dir_path = dir_path + "/results2.txt"
    with open(dir_path, "r") as file:
        for line in file:
            line_s = json.loads(line)
            if line_s["p_typo"] == to_check:
                suggested_package = line_s["real_project"]
                mal_type = lambda x: "typosquat" if line_s["typosquat"] == True else "namesquat"
                mal_type = mal_type(line_s["typosquat"])
                ask_to_continue()


def ask_to_continue():
    write_output(
        "Maybe you have meant: " + suggested_package + "?" + " If you wish to " + command + " " +
        suggested_package + " instead, type: 'a'  correctly")
    write_output(
        "The package: " + package_name + " you about to " + command + " is flaged as a " +
        mal_type + " and may has mal. code inside")
    yes_no = input("Do you wish to continue, your " + command + " (y/n/a)?")
    if yes_no == "y":
        pass
    elif yes_no == "n":
        raise CollidingNameError(package_name, suggested_package)
    elif yes_no == "a":
        return suggested_package
    else:
        raise BadCommand
