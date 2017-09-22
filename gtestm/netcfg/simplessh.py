#!/usr/bin/env python3
import paramiko

import gtestm.netcfg.config as config


def run(cmd: str, cfg: config.Config):
    """
    Wrapper for paramiko's ssh exec_command function.
    :param cmd: Command to run on a remote
    :param cfg: Configuration data
    :return: A 4-tuple of indata, outdata, errdata, ssh_channel
    """
    ssh = auth(cfg)
    ind, outd, errd = ssh.exec_command(cmd)
    return ind, outd, errd, ssh


def auth(cfg: config.Config):
    """
    Based on a provided configuration, connect using an ssh connection
    :param cfg: Configuration to use while connecting
    :return: The ssh session that was opened
    """
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(hostname=cfg.remote_host, username=cfg.remote_user, password=cfg.remote_pass)
    return ssh


def paaf(f: iter):
    """
    Print everything in a given iterable of string-decodable objects
    :param f: The iterable being printed
    :return: None
    """
    print(*[x.decode("utf-8") for x in f.read().splitlines()], sep="\n")
