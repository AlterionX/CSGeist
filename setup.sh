#!/usr/bin/env bash
pip3 install paramiko
cp config-sample config
vim -O README.md config guide.txt
echo "Run \"python3 -m gtestm.main -m cli\" for cli"
echo "Run \"python3 -m gtestm.main -m gui_utils\" for gui_utils"
echo "Running \"python3 -m gtest.main\" will launch the cli"

