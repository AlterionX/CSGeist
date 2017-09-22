#!/usr/bin/env python3

import stat

import gtestm_netcfg.config as config
import gtestm_netcfg.simplessh as genssh


def paaf(f):
    print(*[x.decode("utf-8") for x in f.read().splitlines()], sep="\n")


class TestData:
    def __init__(self):
        self.tests = {}
        self.passed = 0
        self.failed = 0
        self.total = 0
        self.timed_out = 0
        self.comp_failed = 0

    def update(self, file_hash, data):
        self.total += 1
        for i in range(len(data)):
            print(i, data[i])
        if "... pass ---" == data[0][-len("... pass ---"):len(data[0])]:
            print("Passed!")
            self.tests[file_hash] = "pass", data
            self.passed += 1
        elif "----> timeout <----" == data[-1][-len("----> timeout <----"):len(data[-1])]:
            print("Timed out!")
            self.tests[file_hash] = "timed_out", data
            self.timed_out += 1
        elif "... fail ---" == data[0][-len("... pass ---"):len(data[0])]:
            print("Failed!")
            self.tests[file_hash] = "fail", data
            self.failed += 1
        elif "failed" == data[-1][-len("failed"):len(data[-1])] and "Makefile:32: recipe for target " == data[-1][:len(
                "Makefile:32: recipe for target ")]:
            print("Compilation failed!")
            self.tests[file_hash] = "comp_failed", data
            self.comp_failed += 1

    def __str__(self):
        print(
            "Total: {} Passed: {} Failed: {} Timed Out: {} Compilation with makefile failed: {}".format(
                self.total,
                self.passed,
                self.failed,
                self.timed_out,
                self.comp_failed
            )
        )


def runtests_remoteserial(cfg: config.Config):
    remote_test_dir = "/v/filer5b/v41q001/gheith/public/{}_{}_{}".format(
        cfg.curr_proj_cls,
        cfg.curr_proj_sem,
        cfg.curr_proj_num
    )
    prep_cmd = "mkdir {};cd {};cp -r {}/* {};cp -r {}/* {};echo \"Completion\"".format(
        cfg.outp_dir,
        cfg.outp_dir,
        remote_test_dir,
        cfg.outp_dir,
        cfg.proj_dir,
        cfg.outp_dir
    )

    indata, outdata, errdata, ssh = genssh.run(cmd=prep_cmd, cfg=cfg)
    paaf(outdata)
    ssh.close()

    ssh = genssh.auth(cfg)
    sftp = ssh.open_sftp()
    sftp.chdir(remote_test_dir)

    tests = TestData()

    for direc in sftp.listdir_iter():
        if not stat.S_ISDIR(direc.st_mode):
            ssh = genssh.auth(cfg)
            print("making " + direc.filename[:direc.filename.index('.')])
            indata, outdata, errdata = ssh.exec_command(
                "cd {};make -s {}.result".format(
                    cfg.outp_dir,
                    direc.filename[:direc.filename.index('.')]
                )
            )
            data = [x.decode("utf-8") for x in outdata.read().splitlines()]
            tests.update(direc.filename[:direc.filename.index('.')], data)
            ssh.close()

    sftp.close()

    return tests


if __name__ == "__main__":
    config = config.Config()
    runtests_remoteserial(config)
