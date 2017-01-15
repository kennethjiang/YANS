import docker

from logging import debug
import sys
import subprocess
import os

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
        docker_machine_run('sudo brctl addbr ' + lnk.bridge_name)
        docker_machine_run('sudo ip link set ' + lnk.bridge_name + ' up')

def destroy_links(links):
    for lnk in links:
        docker_machine_run('sudo ip link set ' + lnk.bridge_name + ' down')
        docker_machine_run('sudo brctl delbr ' + lnk.bridge_name)

def create_nodes(nodes):
    client().images.pull('kennethjiang/yans-node')
    for node in nodes:
        client().containers.run('kennethjiang/yans-node', name=node.container_name, command='sleep 3153600000', detach=True, privileged=True)

def destroy_nodes(nodes):
    for node in nodes:
        try:
            client().containers.get(node.container_name).remove(force=True)
        except docker.errors.NotFound:
            pass

def attach_node(node):
    set_docker_machine_env()
    import shlex
    subprocess.call(shlex.split('docker exec -it --privileged ' + node.container_name + ' bash'), stdin=sys.stdin, stdout=sys.stdout)

def bind_interface(interface):
    docker_machine_run('sudo ip link add ' + interface.name + ' type veth peer name ' + interface.peer_name)
    docker_machine_run('sudo ip link set ' + interface.peer_name + ' up')
    docker_machine_run('sudo brctl addif ' + interface.link.bridge_name + ' ' + interface.peer_name)
    container_pid = str(client().api.inspect_container( interface.node.container_name )['State']['Pid'])
    docker_machine_run('sudo ip link set netns ' + container_pid + ' dev ' + interface.name)

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
        set_docker_machine_env()
        docker_client = docker.from_env()

def set_docker_machine_env():
    if not is_linux():
        out = run('docker-machine env YANS-machine')
        import re
        for (name, value) in re.findall('export ([^=]+)="(.+)"', out):
            os.environ[name] = value
