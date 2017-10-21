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
    def __init__(self, cfg: config.Config, td, sd, target, hashlist=None):
        """
        Initialize the runnable
        :param cfg: configuration data
        """
        super().__init__(name="TestRunner")
        self.cfg = cfg
        self.td = td
        self.sd = sd
        self.report = target
        self.hashlist = hashlist
        self.daemon = True

    def run(self):
        self.report.event_generate("<<StartSetUp>>")
        try:
            direc = gen.direc_setup(self.cfg, multi=self.cfg.SIMULT)
        except RuntimeError:
            self.report.event_generate("<<EndUpdate-FAIL>>")
            return -1
        self.report.event_generate("<<StartFetch>>")
        try:
            sublist = gen.fetch_direc_list(self.cfg, direc)
        except IOError:
            self.report.event_generate("<<EndUpdateWrongDir>>")
            return
        hashset = set(self.hashlist if self.hashlist is not None else [
            direc.filename[:direc.filename.index(".")]
            for direc in sublist
        ])
        self.report.event_generate("<<StartRun>>")
        try:
            parallel.parallel_run(
                self.cfg, self.td, self.sd,
                prog_report=lambda: self.report.event_generate("<<Updated>>"),
                remote_test_dir=direc, jobset=hashset
            )
        except RuntimeError:
            self.report.event_generate("<<EndUpdate-FAIL>>")
            return
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

    def do_refresh(self, trigger, hashlist=None):
        if self.cfg.check_req():
            trigger.event_generate("<<ReqData>>")
            return False
        if self.run_lock.acquire(blocking=False):
            self.testdata = testdata.TestData()
            self.run_thread = TestRunner(self.cfg, self.testdata, self.statedata, trigger, hashlist=hashlist)
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
