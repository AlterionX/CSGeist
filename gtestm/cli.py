#!/usr/bin/env python3
from argparse import Namespace

from gtestm.netcfg import config
from gtestm.run import linear
from gtestm.run import parallel
from gtestm.utils import testdata


def linear_(cfg: config.Config):
    linear.linear_run(cfg, testdata.TestData(), testdata.StateData())


def main(args: Namespace, cfg: config.Config):
    sd = testdata.StateData()
    td = parallel.parallel_run(cfg, testdata.TestData(), sd, multi=args.parallel_count)
    print(td)


if __name__ == "__main__":
    print("Please launch main.py, instead, with the following command: ./main.py")
