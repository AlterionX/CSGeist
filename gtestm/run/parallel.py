import queue
import threading

from gtestm.run import general as gen
from gtestm.utils import utlab

runlock = threading.Lock()


class TestJob:
    def __init__(self, name, cfg):
        self.name = name
        self.cfg = cfg

    def run(self, num, machine, rq):
        data = (
            self.name,
            gen.single_run(
                self.name, self.cfg, multi=num, otherhost="{}.cs.utexas.edu".format(machine.host)
            )
        )
        print(self.name, data)
        rq.put(data)


class TestThread(threading.Thread):
    def __init__(self, num, machine, resultqueue, jq):
        super().__init__()
        self.jq = jq
        self.num = num
        self.machine = machine
        self.resultqueue = resultqueue

    def run(self):
        while True:
            try:
                job = self.jq.get(timeout=1)
            except queue.Empty:
                break
            if job is None:
                break
            job.run(num=self.num, machine=self.machine, rq=self.resultqueue)
            self.jq.task_done()


def parallel_run(cfg, td, sd, multi=10):
    runlock.acquire()
    remote_test_dir = gen.direc_setup(cfg, multi=multi)

    tests = gen.fetch_test_list(cfg, remote_test_dir)
    sd.set_q(len(tests))

    rq = queue.Queue()
    jq = queue.Queue()

    for test in tests:
        jq.put(TestJob(test, cfg))

    machines = utlab.grab_all()
    for i in range(cfg.SIMULT):
        TestThread(i, machines[i], rq, jq).start()

    while not jq.empty():
        data = rq.get()
        td.update(*data)

    jq.join()

    while True:
        try:
            data = rq.get(timeout=5)
        except queue.Empty:
            break
        td.update(*data)

    runlock.release()

    return td
