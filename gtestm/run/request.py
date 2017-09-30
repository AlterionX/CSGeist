import threading as th

from gtestm.netcfg import config
from gtestm.utils import testdata
from gtestm.run import general as gen
from gtestm.run import parallel


class TkStateData(testdata.StateData):
    def __init__(self, quant, progress):
        super().__init__(quant=quant, progress=progress)

    def set_q(self, q):
        self.quant.set(q)

    def incre_p(self):
        self.proglock.acquire()
        self.progress.set(self.progress.get() + 1)
        self.proglock.release()

    def reset_p(self):
        self.proglock.acquire()
        self.progress.set(0)
        self.proglock.release()


class TestRunner(th.Thread):
    def __init__(self, cfg: config.Config, td, sd, target):
        """
        Initialize the runnable
        :param cfg: configuration data
        :param hashlist: List of files to run on
        """
        super().__init__(name="TestRunner")
        self.cfg = cfg
        self.td = td
        self.sd = sd
        self.report = target
        self.daemon = True

    def run(self, hashlist=None):
        self.report.event_generate("<<StartSetUp>>")
        direc = gen.direc_setup(self.cfg)
        self.report.event_generate("<<StartFetch>>")
        hashset = set(hashlist if hashlist is not None else [
            direc.filename[:direc.filename.index(".")]
            for direc
            in gen.fetch_direc_list(self.cfg, direc)
        ])
        self.report.event_generate("<<StartRun>>")
        parallel.parallel_run(
            self.cfg, self.td, self.sd,
            prog_report=lambda: self.report.event_generate("<<Updated>>"),
            remote_test_dir=direc, jobset=hashset
        )
        self.report.event_generate("<<EndUpdate>>")


class Backend:
    def __init__(self, tksd: testdata.StateData, td: testdata.TestData, cfg: config.Config = None):
        if cfg is None:
            cfg = config.Config(delay_login=True)
        self.cfg = cfg
        self.testdata = td
        self.statedata = tksd
        self.run_thread = th.Thread()
        self.run_lock = th.Lock()

    def do_full_refresh(self, trigger):
        if self.cfg.check_req():
            trigger.event_generate("<<ReqData>>")
            return False
        if self.run_lock.acquire(blocking=False):
            self.testdata = testdata.TestData()
            self.run_thread = TestRunner(self.cfg, self.testdata, self.statedata, trigger)
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
