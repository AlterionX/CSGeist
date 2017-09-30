#!/usr/bin/env python3
import paramiko

from gtestm.netcfg import config
from gtestm.utils import utlab


def run(cmd: str, cfg: config.Config, otherhost=None):
    """
    Wrapper for paramiko's ssh exec_command function.
    :param otherhost:
    :param cmd: Command to run on a remote
    :param cfg: Configuration data
    :return: A 4-tuple of indata, outdata, errdata, ssh_channel
    """
    if otherhost is None:
        machines = utlab.grab_all()
        otherhost = "{}.cs.utexas.edu".format(machines[0].host)
    ssh = auth(cfg, otherhost)
    ind, outd, errd = ssh.exec_command(cmd)
    return ind, outd, errd, ssh


def auth(cfg: config.Config, otherhost=None):
    """
    Based on a provided configuration, connect using an ssh connection
    :param otherhost:
    :param cfg: Configuration to use while connecting
    :return: The ssh session that was opened
    """
    if otherhost is None:
        machines = utlab.grab_all()
        otherhost = "{}.cs.utexas.edu".format(machines[0].host)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(hostname=otherhost, username=cfg.remote_user, password=cfg.remote_pass)
    return ssh


def paaf(f: iter):
    """
    Print everything in a given iterable of string-decodable objects
    :param f: The iterable being printed
    :return: None
    """
    print(*[x.decode("utf-8") for x in f.read().splitlines()], sep="\n")
