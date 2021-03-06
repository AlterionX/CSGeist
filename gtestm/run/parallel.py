import queue
import threading

from gtestm.run import general as gen
from gtestm.utils import utlab
from gtestm.netcfg import config
from gtestm.utils import testdata

runlock = threading.Lock()


class TestJob:
    def __init__(self, name, cfg):
        self.name = name
        self.cfg = cfg

    def run(self, num, machine, rq):
        data = gen.single_run(
            self.name, self.cfg, multi=num, otherhost="{}.cs.utexas.edu".format(machine.host)
        )
        data = (
            self.name,
            data
        )
        rq.put(data)


class TestThread(threading.Thread):
    def __init__(self, num, machine, resultqueue, jq):
        super().__init__(name="Testing{}".format(num))
        self.jq = jq
        self.num = num
        self.machine = machine
        self.resultqueue = resultqueue
        self.daemon = True

    def run(self):
        while True:
            job = self.jq.get()
            if job is None:
                self.jq.task_done()
                break
            try:
                job.run(num=self.num, machine=self.machine, rq=self.resultqueue)
            except RuntimeError:
                print("Terminating thread")
                return
            self.jq.task_done()


def parallel_run(
        cfg: config.Config,
        td: testdata.TestData, sd: testdata.StateData,
        remote_test_dir=None,
        multi=10, jobset: set = None,
        prog_report: callable = None
):
    runlock.acquire()

    if remote_test_dir is None:
        remote_test_dir = gen.direc_setup(cfg, multi=multi)

    if jobset is None:
        jobset = gen.fetch_test_list(cfg, remote_test_dir)

    tests = jobset
    sd.set_q(len(tests))
    sd.reset_p()

    rq = queue.Queue()
    jq = queue.Queue()

    for test in tests:
        jq.put(TestJob(test, cfg))

    print("Grabbing machines")

    machines = utlab.grab_all()
    threads = []
    for i in range(multi):
        jq.put(None)
        threads.append(TestThread(i, machines[i], rq, jq))
        threads[-1].start()

    print("Started everything")

    while not jq.empty():
        data = rq.get()
        td.update(*data)
        sd.incre_p()
        if prog_report is not None:
            prog_report()

    jq.join()

    while not rq.empty():
        data = rq.get()
        td.update(*data)
        sd.incre_p()
        if prog_report is not None:
            prog_report()

    runlock.release()

    return td
