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
from subprocess import check_call


__version__ = "0.1.0"
__author__ = "Kenneth Jiang"
__license__ = "MIT"

PREFIX = 'yans_'

def cmd(cmd, cont=False):
    import shlex
    args = shlex.split(cmd)
    check_call(args)

def create_links(links):
    for lnk in links:
	lnk_name = PREFIX + lnk['name']
        cmd('docker network create --driver=bridge ' + lnk_name)
	
def destroy_links(links):
    for lnk in links:
        lnk_name = PREFIX + lnk['name']
        cmd('docker network rm ' + lnk_name)

def main():
    '''Main entry point for the yans CLI.'''
    args = docopt(__doc__, version=__version__)
    print(args)

    with open(args['--topo'], 'r') as f:
        links = yaml.load(f)

    import pdb; pdb.set_trace()
    if args['up']:
	create_links(links)
    if args['destroy']:
        destroy_links(links)

if __name__ == '__main__':
    main()
