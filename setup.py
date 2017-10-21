#!/usr/bin/env python3
import getpass
import pathlib
import subprocess

import netcfg.config as cfg

# Install needed packages
subprocess.run("pip3 install paramiko", shell=True)
subprocess.run("pip3 install bs4", shell=True)

# Check if config file exists, or config-sample exists
file_path = ""
while not file_path:
    file_path = input(
        "Please enter a path to use as the configuration file's basis or press enter to continue:\n"
    ).strip()
    if not file_path:
        print("Using default file paths. Looking for old configuration files...")
        file_path = pathlib.Path("./config")
        if not file_path.exists() or not file_path.is_file():
            print("No old file located. Searching for sample configuration file...")
            file_path = pathlib.Path("./config-sample")
            if not file_path.exists() or not file_path.is_file():
                print("Unable to locate any old files. Restarting from scratch.")
                file_path = pathlib.Path("./config")
                file_path.touch()
                file_path.write_text("Hello world, will be overwritten soon by configuration details (hopefully).")
            else:
                print("Using default sample file as basis.")
        else:
            print("Using old configuration file as basis.")
    else:
        print("Using following path:", file_path)
        file_path = pathlib.Path(file_path)
        if not file_path.exists() or not file_path.is_file():
            file_path = ""

# Now has a valid end goal

cfg.Config(cfg_file=file_path, delay_login=True)

data = {}

for subject, text, secure in cfg.Config.REQ_ELEM:
    value = ""
    if not secure:
        value = input(
            "Current data stored for {} is {}.\nThis is{} please enter a value:".format(
                subject, cfg.Config.ENV_VARS[subject], text
            )
        ).strip()
    else:
        value = getpass.getpass()
    if value:
        data[subject] = value
    else:
        data[subject] = cfg.Config.ENV_VARS[subject]

with open("./config", mode="w") as config_file:
    for subject in data:
        print("New stuff for {} is {}".format(subject, data[subject]))
        config_file.write("{}:{}\n".format(subject, "" if data[subject] is None else data[subject]))
