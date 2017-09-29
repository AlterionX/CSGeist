#!/usr/bin/env python3
from argparse import Namespace

from gtestm.netcfg import config
from gtestm.run.parallel import parallel_run
from gtestm.utils import testdata
from run import general


def main(args: Namespace, cfg: config.Config):
    sd = testdata.StateData()
    td = parallel_run(cfg, testdata.TestData(), sd, multi=args.multi)


if __name__ == "__main__":
    print("Please launch main.py, instead, with the following command: main.py")
