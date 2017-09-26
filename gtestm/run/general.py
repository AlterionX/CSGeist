import stat

from netcfg import config
from utils import testdata
from netcfg import simplessh as genssh


def fetch_direc_list(cfg: config.Config, direc: str, all=False):
    ssh = genssh.auth(cfg)
    sftp = ssh.open_sftp()
    sftp.chdir(direc)
    if not all:
        direcs = list(filter(lambda direc: not stat.S_ISDIR(direc.st_mode), sftp.listdir_attr()))
    else:
        direcs = sftp.listdir_attr()
    sftp.close()
    return direcs


def fetch_test_list(cfg: config.Config, direc: str):
    return list(set(map(
        lambda direc: direc.filename[:direc.filename.index('.')],
        fetch_direc_list(cfg, direc, False)
    )))


def single_run(filename: str, cfg: config.Config, td: testdata.TestData = None, multi=None, otherhost=None):
    if otherhost is None:
        otherhost = cfg.remote_host
    name = filename if '.' not in filename else filename[:filename.index('.')]
    cmd_str = "cd {}".format(cfg.outp_dir)
    if multi:
        cmd_str += "/CSGeist_m{};mv ../{}.* ./".format(multi, name)

    cmd_str += ";make -s {}.result".format(name)

    if multi:
        cmd_str += ";mv ./{}.* ../".format(name)

    indata, outdata, errdata, ssh = genssh.run(
        cmd_str,
        cfg,
        otherhost
    )
    data = [x.decode("utf-8") for x in outdata.read().splitlines()]
    if td is None:
        return data
    td.update(name, data)
    ssh.close()


def direc_setup(cfg: config.Config, multi=None):
    remote_test_dir = "{}/{}_{}_{}".format(
        cfg.test_dir,
        cfg.curr_proj_cls,
        cfg.curr_proj_sem,
        cfg.curr_proj_num
    )
    prep_cmd = "mkdir {};cd {};cp -r {}/* ./".format(
        cfg.outp_dir,
        cfg.outp_dir,
        remote_test_dir,
        cfg.outp_dir
    )

    if multi is not None:
        for i in range(multi):
            prep_cmd += ";mkdir ./CSGeist_m{};cp -r {}/{}_{}_{}_{}/* ./CSGeist_m{}".format(
                i,
                cfg.proj_dir,
                cfg.remote_user,
                cfg.curr_proj_cls,
                cfg.curr_proj_sem,
                cfg.curr_proj_num,
                i
            )
    else:
        prep_cmd += ";cp -r {}/{}_{}_{}_{}/* ./".format(
            cfg.proj_dir,
            cfg.remote_user,
            cfg.curr_proj_cls,
            cfg.curr_proj_sem,
            cfg.curr_proj_num
        )

    _, output, _, ssh = genssh.run(cmd=prep_cmd, cfg=cfg)
    ssh.close()

    _, output, _, ssh = genssh.run("readlink -f {}".format(remote_test_dir), cfg)
    remote_test_dir = output.read().strip().decode()
    ssh.close()

    return remote_test_dir


if __name__ == "__main__":
    print("Please run one of the files in the modes module.")
