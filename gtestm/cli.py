#!/usr/bin/env python3
from argparse import Namespace

from gtestm.netcfg import config
from gtestm.run.parallel import parallel_run
from gtestm.utils import testdata


def main(args: Namespace, cfg: config.Config):
    flags = {}

    td = testdata.TestData()
    sd = testdata.StateData()
    td = parallel_run(cfg, td, sd, multi=args.multi)


if __name__ == "__main__":
    print("Please launch main.py, instead, with the following command: main.py")
