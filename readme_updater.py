from cache_manager import get_packages
from configparser import ConfigParser
from configparser import ExtendedInterpolation
import glob
from os import getlogin
import pickle

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read("config.ini")
packages = get_packages(
    "scripts/", str(config["PACKAGES"]["ignore"]).split(sep=", "))

readme_path = config["COMMON"]["readme_path"].replace(
    "~", "/home/" + getlogin())
start_update = True
continue_read = True
readme_updated = list()
with open(readme_path, "r") as readme:
    for line in readme.readlines():
        if not continue_read:
            if start_update:
                for package_counter in packages:
                    readme_updated.append(
                        str("- {0} - {1} - {2}".format(
                            packages[package_counter][0].capitalize(),
                            packages[package_counter][1],
                            packages[package_counter][2])))
                start_update = False
            if line == "<!--readme_update end -->\n":
                readme_updated.append(line)
                continue_read = True
        else:
            continue_read = line != "<!--readme_update start -->\n"
            readme_updated.append(line)
del start_update, continue_read

with open(readme_path, "w") as readme:
    for line in readme_updated:
        print(line.strip("\n"), file=readme)
del readme_path, readme_updated
