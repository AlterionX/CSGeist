#!/usr/bin/env python3
import time

from gtestm.netcfg import config
from gtestm.modes import cli
from gtestm.run import general
from gtestm.utils import testdata


def comp_serial_parallel():
    cfg = config.Config()

    serial_td = testdata.TestData()
    parallel_td = testdata.TestData()

    serial_sd = testdata.StateData()
    parallel_sd = testdata.StateData()

    start = time.time()
    print("Starting serial tests")
    print(cli.linear_run(cfg, serial_td, serial_sd))
    serial_rt = time.time() - start
    print("Took", time.time() - start, "seconds")
    print("Starting parallel tests")
    start = time.time()
    print(cli.parallel_run(cfg, parallel_td, parallel_sd))
    parallel_rt = time.time() - start
    print("Took", time.time() - start, "seconds")
    print("Serial runs:", serial_rt)
    print("Parallel runs:", parallel_rt)
    print("Differs by", serial_rt - parallel_rt, "seconds.")
    for file in serial_td.tests:
        s_t = serial_td.tests[file]
        p_t = parallel_td.tests[file]
        print(s_t)
        print(p_t)


def parallel_check():
    cfg = config.Config()

    parallel_td = testdata.TestData()
    parallel_sd = testdata.StateData()

    tests = general.fetch_test_list(cfg, general.direc_setup(cfg, multi=10))
    print(tests[0])

    print(cli.parallel_run(cfg, parallel_td, parallel_sd))

    for test in tests:
        if test not in parallel_td.tests:
            print(test)


if __name__ == "__main__":
    parallel_check()
    input("Enter to proceed")
    comp_serial_parallel()
