import threading as th

from gtestm.netcfg import config
from gtestm.utils import testdata
from gtestm.run import general as gen

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
                in gen.fetch_direc_list(self.cfg, gen.direc_setup(cfg))
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
            gen.single_run(direc, self.cfg, td=self.td)
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
        self.cfg = config.Config(delay_login=True)
        self.testdata = testdata.TestData()
        self.run_thread = th.Thread()
        self.localstore = th.local
        self.run_lock = th.Lock()

    def do_full_refresh(self, trigger):
        if self.cfg.check_req():
            trigger.event_generate("<<ReqData>>")
            return False
        if self.run_lock.acquire(blocking=False):
            self.testdata = testdata.TestData()
            self.run_thread = TestAllRunner(self.cfg, self.testdata, trigger)
            self.run_thread.start()
            self.run_lock.release()
            return True
        else:
            return False

    def get_tests(self):
        return self.testdata.tests

    def set_profile(self, usern, passw):
        self.cfg.remote_user = usern
        self.cfg.remote_pass = passw
        self.cfg.store[config.Config.GDC_USER_KEY] = self.cfg.remote_user
        self.cfg.store[config.Config.GDC_PASS_KEY] = self.cfg.remote_pass
