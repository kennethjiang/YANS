import docker

from logging import debug
import sys
import subprocess
import os

PREFIX = 'YANS-'

docker_client = None

def exists(exe):
    return any(os.access(os.path.join(path, exe), os.X_OK) for path in os.environ["PATH"].split(os.pathsep))

def is_linux():
    return sys.platform == 'linux' or sys.platform == 'linux2'

def run(cmd, cont=False):
    debug('Running command: ' + cmd)

    import shlex
    args = shlex.split(cmd)
    if cont:
        return subprocess.call(args, stdout=open(os.devnull, 'w'))
    else:
        return subprocess.check_output(args)

def docker_machine_run(cmd):
    if is_linux():
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
    dc = client()
    dc.images.pull('kennethjiang/yans-node')
    for node in nodes:
        node_name = PREFIX + node
        dc.containers.run('kennethjiang/yans-node', name=node_name, command='sleep 3153600000', detach=True, privileged=True)

def destroy_nodes(nodes):
    dc = client()
    for node in nodes:
        node_name = PREFIX + node
        try:
            dc.containers.get(node_name).remove(force=True)
        except docker.errors.NotFound:
            pass

def ensure_docker_machine():
    if is_linux(): # docker machine not required on linux
        return
def ensure_docker_machine():
    if is_linux(): # docker machine not required on linux
        return

    if not exists('docker-machine'):
        sys.exit("docker-machine is required to run yans on Mac OS X. Please make sure it is installed and in $PATH")

    if run('docker-machine inspect YANS-machine', cont=True) != 0: # create docker machine needed for YANS if one doesn't exist
        print('Creating docker machine that will host all YANS containers')
        run('docker-machine create -d virtualbox --virtualbox-boot2docker-url https://github.com/kennethjiang/YANS/raw/master/boot2docker/boot2docker.iso YANS-machine')

    run('docker-machine start YANS-machine', cont=True) # make sure YANS-machine is started


def client():
    ensure_docker_client()
    return docker_client

def ensure_docker_client():
    global docker_client
    if not docker_client:
        if not is_linux():
            out = run('docker-machine env YANS-machine')
            import re
            for (name, value) in re.findall('export ([^=]+)="(.+)"', out):
                os.environ[name] = value

        docker_client = docker.from_env()
