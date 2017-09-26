#!/usr/bin/env python3
import sys

import gtestm.netcfg.config as config
from gtestm.utils import testdata
from run.parallel import parallel_run
from run.linear import linear_run


def main(args: list):
    flags = {}
    for i in range(len(args)):
        if sys.argv[i].index("-") == 0:
            addi = None
            if i + 1 < len(sys.argv) and sys.argv[i + 1][0] != '-':
                addi = sys.argv[i + 1]
            # flags
            for c in sys.argv[i][1:]:
                flags[c] = addi

    if 'c' in flags:
        cfg = config.Config(cfg_file=flags['c'])
    else:
        cfg = config.Config()

    td = testdata.TestData()
    sd = testdata.StateData()

    if 's' in flags:
        td = linear_run(cfg, td, sd)
    elif 'p' in flags:
        if flags['p'] is None:
            flags['p'] = cfg.SIMULT
        td = parallel_run(cfg, td, sd, multi=flags['p'])
    else:
        td = parallel_run(cfg, td, sd, multi=cfg.SIMULT)
    print(td)


if __name__ == "__main__":
    main(sys.argv[1:])
