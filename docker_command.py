import docker

import logging
import sys
import subprocess
import os

PREFIX = 'YANS-'

client = None

def exists(exe):
    return any(os.access(os.path.join(path, exe), os.X_OK) for path in os.environ["PATH"].split(os.pathsep))

def run(cmd, cont=False):
    logging.debug('Running command: ' + cmd)

    import shlex
    args = shlex.split(cmd)
    if cont:
        return subprocess.call(args, stdout=open(os.devnull, 'w'))
    else:
        return subprocess.check_output(args)

def docker_machine_run(cmd):
    if sys.platform == 'linux' or sys.platform == 'linux2':
        return run(cmd)
    else:
        return run('docker-machine ssh YANS-machine ' + cmd)

def create_links(links):
    for lnk in links:
        lnk_name = PREFIX + lnk['name']
        docker_machine_run('sudo /usr/local/sbin/brctl addbr ' + lnk_name)
        docker_machine_run('sudo /usr/local/sbin/ip link set ' + lnk_name + ' up')

def destroy_links(links):
    for lnk in links:
        lnk_name = PREFIX + lnk['name']
        docker_machine_run('sudo /usr/local/sbin/ip link set ' + lnk_name + ' down')
        docker_machine_run('sudo /usr/local/sbin/brctl delbr ' + lnk_name)

def create_nodes(nodes):
    pass


def ensure_docker_machine():
    if sys.platform == 'linux' or sys.platform == 'linux2': # docker machine not required on linux
        return

    if not exists('docker-machine'):
        sys.exit("docker-machine is required to run yans on Mac OS X. Please make sure it is installed and in $PATH")

    if run('docker-machine inspect YANS-machine', cont=True) != 0: # create docker machine needed for YANS if one doesn't exist
        print('Creating docker machine that will host all YANS containers')
        run('docker-machine create -d virtualbox --virtualbox-boot2docker-url https://github.com/kennethjiang/YANS/raw/master/boot2docker/boot2docker.iso YANS-machine')

    run('docker-machine start YANS-machine', cont=True) # make sure YANS-machine is started


def ensure_client():
    global client
    if not client:
        out = run('docker-machine env YANS-machine')
        import re
        for (name, value) in re.findall('export ([^=]+)=(.+)', out):
            os.environ[name] = value

        client = docker.from_env()
