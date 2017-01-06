import docker

from logging import debug
import sys
import subprocess
import os
import uuid
import string

PREFIX = 'YANS-'

docker_client = None

def random_id(size=6, chars=string.letters + string.digits):
    import random
    return ''.join(random.choice(chars) for _ in range(size))

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

def bridge_name(link):
    return PREFIX + link['name']

def create_links(links):
    for lnk in links:
        docker_machine_run('sudo /usr/local/sbin/brctl addbr ' + bridge_name(lnk))
        docker_machine_run('sudo /usr/local/sbin/ip link set ' + bridge_name(lnk) + ' up')

def destroy_links(links):
    for lnk in links:
        docker_machine_run('sudo /usr/local/sbin/ip link set ' + bridge_name(lnk) + ' down')
        docker_machine_run('sudo /usr/local/sbin/brctl delbr ' + bridge_name(lnk))

def create_nodes(nodes):
    client().images.pull('kennethjiang/yans-node')
    for node in nodes:
        node_name = PREFIX + node
        client().containers.run('kennethjiang/yans-node', name=node_name, command='sleep 3153600000', detach=True, privileged=True)

def destroy_nodes(nodes):
    dc = client()
    for node in nodes:
        node_name = PREFIX + node
        try:
            dc.containers.get(node_name).remove(force=True)
        except docker.errors.NotFound:
            pass

def link_node(link, node):
    if_name = 'yans' + random_id()
    if_peer = if_name + '-p'
    docker_machine_run('sudo /usr/local/sbin/ip link add ' + if_name + ' type veth peer name ' + if_peer)
    docker_machine_run('sudo /usr/local/sbin/ip link set ' + if_peer + ' up')
    docker_machine_run('sudo /usr/local/sbin/brctl addif ' + bridge_name(link) + ' ' + if_peer)
    container_pid = str(client().api.inspect_container(node)['State']['Pid'])
    docker_machine_run('sudo /usr/local/sbin/ip link set netns ' + container_pid + ' dev ' + if_name)

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
