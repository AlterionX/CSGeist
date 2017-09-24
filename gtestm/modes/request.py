#!/usr/bin/env python3
import stat
import threading as th

import gtestm.netcfg.config as config
import gtestm.utils.testdata as testdata
import gtestm.modes.run as run
import gtestm.modes.run as runmet


proglock = th.Lock()
progress = None
quant = 0


class TestAllRunner(th.Thread):
    def __init__(self, cfg: config.Config, td, target, hashlist=None):
        """
        Initialize the runnable
        :param cfg: configuration data
        :param hashlist: List of files to run on
        """
        super().__init__()
        self.cfg = cfg
        self.hashset = set(hashlist) if hashlist is not None else set(
            [
                direc.filename[:direc.filename.index(".")]
                for direc
                in filter(
                    lambda direc: not stat.S_ISDIR(direc.st_mode),
                    runmet.fetch_direc_list(self.cfg, runmet.direc_setup(cfg))
                )
            ]
        )
        self.td = td
        self.report = target
        self.daemon = True

    def run(self):
        global proglock
        global progress
        global quant
        proglock.acquire()
        progress = 0
        proglock.release()
        quant = len(self.hashset)
        for direc in self.hashset:
            print(direc)
            run.run_test_single(direc, self.cfg, self.td)
            progress = self.td.total
            self.report.event_generate("<<Updated>>")
        self.report.event_generate("<<EndUpdate>>")


class TestSingleRunner(TestAllRunner):
    def __init__(self, cfg: config.Config, td, target, hashstr):
        """
        Initialize the data needed for a single test
        :param cfg: Configuration data for the test
        :param hashstr: file name
        """
        super().__init__(cfg, td, target, [hashstr])


class Backend:
    def __init__(self):
        self.cfg = config.Config()
        self.testdata = testdata.TestData()
        self.run_thread = th.Thread()
        self.localstore = th.local
        self.run_lock = th.Lock()

    def do_full_refresh(self, trigger):
        """do_full_refresh() -> None
        no return type, triggers backend to ssh and stuff
        :param self1: """
        if self.run_lock.acquire(blocking=False):
            self.run_thread = TestAllRunner(self.cfg, self.testdata, trigger)
            self.run_thread.start()
            self.run_lock.release()
            return True
        else:
            return False

    def is_refresh_complete(self):
        """is_refresh_complete() -> bool
        True if complete, False otherwise"""
        return not self.run_thread or not self.run_thread.is_alive()

    def get_status(self):
        """
        get_status() -> None | str
        returns a status during the refresh (progress bar %), None if not refreshing
        """
        if not self.run_thread.is_alive():
            return None
        else:
            progrep = 0
            with proglock:
                progrep = progress
            return progrep

    def get_tests(self):
        """get_tests() -> {str : Status}
            returns a dict from hash (str) to Status (enum) and a Flags (class)
            Sorted already
            Status
                PASS
                FAIL
                INVALID
                COMPILE ERR"""
        return self.testdata.tests

    def set_profile(self, usern, passw):
        """
        set_profile(username: str, password: str) -> None"""
        self.cfg.remote_user = usern
        self.cfg.remote_pass = passw

    def run_test(self, hashstr):
        """run_test(hash: str) -> None"""
        if self.run_lock.acquire(blocking=False):
            self.run_thread = th.Thread(target=TestSingleRunner(hashstr))
            self.run_thread.start()
            return True
        else:
            return False

    def get_test_status(self, hashstr):
        """
        get_test_status(hash: str) -> (Status, Flags, ...)
            Status is an enum
                PASS
                FAIL
                TIMEOUT
                COMPILER ERROR
            Flags is a class
                invalid: bool"""
        return self.testdata.tests[hashstr][0], testdata.fetch_flags(hashstr)

    def get_test_data(self, hashstr):
        """
        get_test_data(hash: str) -> returns an array containing three strings:
        First: Test Code
        Second: Expected Output
        Third: Actual Output"""
        data = [x for x in self.testdata.tests[hashstr][3]]
