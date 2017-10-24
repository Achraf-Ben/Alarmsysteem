#!/usr/bin/env python

from fabric.api import run, sudo, task, get, put

env.hosts = ['192.168.1.43']
env.user = 'pi'
env.key_filename = '/home/pi/alarmsystem/keyfile.pem'

def local_uname():
    local('uname -a')

def remote_uname():
    run('uname -a')

remote_uname()
local_uname()

@task
def cmdrun(command):
    """ Usage: fab -H server1,server2 cmdrun:"uptime" """
    run(command)


@task
def sudorun(command):
    """ Usage: fab -H server1,server2 sudorun:"fdisk -l" """
    sudo(command)


@task
def download(path):
    """ Usage: fab -H server1 download:"/path/to/file" """
    get(remote_path=path, local_path="/tmp/", use_sudo=True)


@task
def upload(localpath, remotepath):
    """Usage: fab -H server1,server2 upload:"/localfile","/remote/path/" """
    put(local_path=localpath, remote_path=remotepath, use_sudo=True)
