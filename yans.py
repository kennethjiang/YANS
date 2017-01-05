#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''yans
Yet Another Network Simulator

Usage:
  yans up|stop|destroy [options]
  yans -h | --help
  yans --version

Options:
  -h --help     		Show this screen.
  --version     		Show version.
  -t --topo=<topo_path>  	Network topology YAML [default: ./topo.yaml].
'''

from __future__ import unicode_literals, print_function
from docopt import docopt
import yaml

import sys
import subprocess
import os

__version__ = "0.1.0"
__author__ = "Kenneth Jiang"
__license__ = "MIT"

PREFIX = 'yans_'

def cmd(cmd, cont=False):
    import shlex
    args = shlex.split(cmd)
    if cont:
        return subprocess.call(args, stdout=open(os.devnull, 'w'))
    else:
        return subprocess.check_output(args)

def machine_cmd(cmd):
    if sys.platform == 'linux' or sys.platform == 'linux2':
        return cmd(cmd)
    else
        return cmd('docker-machine ssh YANS-machine ' + cmd)

def create_links(links):
    for lnk in links:
	lnk_name = PREFIX + lnk['name']
        cmd('docker network create --driver=bridge ' + lnk_name)

def destroy_links(links):
    for lnk in links:
        lnk_name = PREFIX + lnk['name']
        cmd('docker network rm ' + lnk_name)

def exists(exe):
    return any(os.access(os.path.join(path, exe), os.X_OK) for path in os.environ["PATH"].split(os.pathsep))

def ensure_docker_machine():
    if sys.platform == 'linux' or sys.platform == 'linux2': # docker machine not required on linux
        return

    if not exists('docker-machine'):
        sys.exit("docker-machine is required to run yans on Mac OS X. Please make sure it is installed and in $PATH")

    if cmd('docker-machine inspect YANS-machine', cont=True) != 0: # create docker machine needed for YANS if one doesn't exist
        print('Creating docker machine that will host all YANS containers')
        cmd('docker-machine create -d virtualbox --virtualbox-boot2docker-url https://github.com/kennethjiang/YANS/raw/master/boot2docker/boot2docker.iso YANS-machine')

    cmd('docker-machine start YANS-machine', cont=True) # make sure YANS-machine is started


def main():
    '''Main entry point for the yans CLI.'''
    args = docopt(__doc__, version=__version__)

    with open(args['--topo'], 'r') as f:
        links = yaml.load(f)

    ensure_docker_machine()

    if args['up']:
	create_links(links)
    if args['destroy']:
        destroy_links(links)

if __name__ == '__main__':
    main()
