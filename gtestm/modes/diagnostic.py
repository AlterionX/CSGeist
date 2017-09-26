#!/usr/bin/env python3
import time

from gtestm.netcfg import config
from gtestm.modes import cli
from gtestm.utils import testdata


def comp_serial_parallel():
    print("Parsing config")
    cfg = config.Config()
    start = time.time()
    print("Starting serial tests")
    print(cli.linear_run(cfg, testdata.TestData(), testdata.StateData()))
    serial_rt = time.time() - start
    print("Took", time.time() - start, "seconds")
    print("Starting parallel tests")
    start = time.time()
    print(cli.parallel_run(cfg, testdata.TestData(), testdata.StateData()))
    parallel_rt = time.time() - start
    print("Took", time.time() - start, "seconds")
    print("Serial runs:", serial_rt)
    print("Parallel runs:", parallel_rt)
    print("Differs by", serial_rt - parallel_rt, "seconds.")


if __name__ == "__main__":
    comp_serial_parallel()
