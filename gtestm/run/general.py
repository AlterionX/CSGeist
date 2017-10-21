import stat

from gtestm.netcfg import config
from gtestm.netcfg import simplessh as genssh
from gtestm.utils import testdata


def fetch_direc_list(cfg: config.Config, direc: str, whole=False):
    ssh = genssh.auth(cfg)
    sftp = ssh.open_sftp()
    sftp.chdir(direc)
    if not whole:
        direcs = list(filter(lambda listed_direc: not stat.S_ISDIR(listed_direc.st_mode), sftp.listdir_attr()))
    else:
        direcs = sftp.listdir_attr()
    sftp.close()
    ssh.close()
    return direcs


def fetch_test_list(cfg: config.Config, direc: str):
    return list(set(map(
        lambda listed_direc: listed_direc.filename[:listed_direc.filename.index('.')],
        fetch_direc_list(cfg, direc, False)
    )))


def single_run(
        filename: str,
        cfg: config.Config,
        td: testdata.TestData = None,
        multi: int = None, otherhost: str = None
):
    if otherhost is None:
        otherhost = cfg.remote_host
    name = filename if '.' not in filename else filename[:filename.index('.')]
    cmd_str = "cd {}".format(cfg.outp_dir)
    if multi is not None:
        cmd_str += "/CSGeist_m{};mv ../{}.{{cc,ok}} ./".format(multi, name)

    cmd_str += ";make clean;make -s {}.result".format(name)

    if multi is not None:
        cmd_str += ";mv ./{}.* ../".format(name)

    cmd_str += ";exit"

    try:
        _, outdata, _, ssh = genssh.run(
            cmd_str,
            cfg,
            otherhost
        )
        data = list(outdata.readlines())
        data = [x.strip() for x in data]
        outdata.channel.recv_exit_status()
        ssh.close()
    except RuntimeError:
        print("Server failed to respond while running a single file.")
        raise RuntimeError("Fuck.")
    print("Finished", filename)

    if td is None:
        return data

    td.update(name, data)


def direc_setup(cfg: config.Config, multi=None):
    remote_test_dir = "{}/{}_{}_{}/latest".format(
        cfg.test_dir,
        cfg.curr_proj_cls,
        cfg.curr_proj_sem,
        cfg.curr_proj_num
    )
    prep_cmd = "cd ~/;rm -rf {};mkdir {};cd {};cp -r {}/* ./".format(
        cfg.outp_dir,
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

    try:
        _, outdata, _, ssh = genssh.run("readlink -f {}".format(remote_test_dir), cfg)
        remote_test_dir = str(outdata.read().strip().decode())
        ssh.close()

        _, outdata, _, ssh = genssh.run(cmd=prep_cmd, cfg=cfg)
        outdata.channel.recv_exit_status()
        ssh.close()
    except RuntimeError:
        print("Failed to setup directory.")
        raise RuntimeError("More fucks.")

    return remote_test_dir


if __name__ == "__main__":
    print("Please run one of the files in the modes module.")
