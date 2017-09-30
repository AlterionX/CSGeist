#!/usr/bin/env python3
import pathlib
import subprocess

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

