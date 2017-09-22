#!/usr/bin/env python3
import paramiko
import gtestm_netcfg.config as config


def run(cmd: str, cfg: config.Config):
    ssh = auth(cfg)
    ind, outd, errd = ssh.exec_command(cmd)
    return ind, outd, errd, ssh


def auth(cfg: config.Config):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(hostname=cfg.remote_host, username=cfg.remote_user, password=cfg.remote_pass)
    return ssh
