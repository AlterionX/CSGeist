#!/usr/bin/env python3
import time

from gtestm import cli
from gtestm.netcfg import config
from gtestm.run import linear
from gtestm.run import general
from gtestm.run import parallel
from gtestm.utils import testdata


def comp_serial_parallel():
    cfg = config.Config()

    serial_td = testdata.TestData()
    parallel_td = testdata.TestData()

    serial_sd = testdata.StateData()
    parallel_sd = testdata.StateData()

    start = time.time()
    print("Starting serial tests")
    print(linear.linear_run(cfg, serial_td, serial_sd))
    serial_rt = time.time() - start
    print("Took", time.time() - start, "seconds")
    print("Starting parallel tests")
    start = time.time()
    print(parallel.parallel_run(cfg, parallel_td, parallel_sd))
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
    
    parallel.parallel_run(cfg, parallel_td, parallel_sd)
    
    return parallel_td


def concurrency_check():
    print("hi")
    td0 = parallel_check()
    print("hi2")
    td1 = parallel_check()
    print("hi")
    for test in td0.tests:
        if td0.tests[test]['status'] != td1.tests[test]['status']:
            print(test)
            print(td0.tests[test]['status'])
            print(td1.tests[test]['status'])
    print("end")


if __name__ == "__main__":
    print("Please launch main.py, instead, with the following command: main.py -m diag")
