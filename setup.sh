#!/usr/bin/env bash
pip3 install paramiko
cp config-sample config
vim -O README.md config guide.txt
echo "Run \"python3 -m gtestm.modes.run\" for cli"
echo "Run \"python3 -m gtestm.gui.gui_util\" for gui"

