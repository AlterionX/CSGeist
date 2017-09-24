#!/usr/bin/env python3
import stat

import gtestm.netcfg.config as config
import gtestm.netcfg.simplessh as genssh
from gtestm.utils import testdata


def fetch_direc_list(cfg: config.Config, direc: str):
    """
    Opens an ssh channel with the provided configuration,
     piggybacks an sftp connection over that, and finally grab a list of
     SFTPAttributes representing all files within that directory.
    :param cfg: Configuration data
    :param direc: Directory stuff
    :return: The list of SFTPAttributes
    """
    ssh = genssh.auth(cfg)
    sftp = ssh.open_sftp()
    sftp.chdir(direc)
    direcs = sftp.listdir_attr()
    sftp.close()
    return direcs


def run_test_single(filename: str, cfg: config.Config, td: testdata.TestData):
    """
    Opens an ssh channel, runs a single test, then closes the channel.
    :param filename: The file to run the test on.
    :param cfg: The configuration data for opening an ssh channel.
    :param td: The TestData object used to hold that tested data
    :return: None
    """
    name = filename if '.' not in filename else filename[:filename.index('.')]
    print("Running test", name)
    indata, outdata, errdata, ssh = genssh.run(
        "cd {};make -s {}.result".format(
            cfg.outp_dir,
            name
        ),
        cfg
    )
    data = [x.decode("utf-8") for x in outdata.read().splitlines()]
    td.update(name, data)
    ssh.close()


def direc_setup(cfg: config.Config):
    """
    Pull on the relevant files into a configured directory, as listed in the configuration object.
    :param cfg: The configuration data for setting up the directory
    :return: The path to gheith's tests
    """
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
    genssh.paaf(outdata)
    ssh.close()
    return remote_test_dir


def run_tests_remote_serial(cfg: config.Config, td: testdata.TestData):
    """
    Run all tests within the remote servers in a serial fashion (not multi-threaded)
    :param cfg: The configuration data for running the tests
    :param td: The TestData object for holding test information
    :return: None
    """
    remote_test_dir = direc_setup(cfg)

    direcs = fetch_direc_list(cfg, remote_test_dir)

    for direc in direcs:
        if not stat.S_ISDIR(direc.st_mode):
            run_test_single(direc.filename, cfg, td)


if __name__ == "__main__":
    config = config.Config()
    run_tests_remote_serial(config, testdata.TestData())
