#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''yans
Yet Another Network Simulator

Usage:
  yans [-V] [-t --topo=<topo_path>] (up|stop|destroy)
  yans -h | --help
  yans --version

Options:
  -h --help                 Show this screen.
  --version                 Show version.
  -t --topo=<topo_path>     Network topology YAML [default: ./topo.yaml].
  -V --verbose              Verbose mode
'''

from __future__ import unicode_literals, print_function
from docopt import docopt
import yaml
import logging

from docker_command import destroy_links, create_nodes, create_links, ensure_docker_machine, destroy_nodes, link_node

__version__ = "0.1.0"
__author__ = "Kenneth Jiang"
__license__ = "MIT"

def main():
    '''Main entry point for the yans CLI.'''
    args = docopt(__doc__, version=__version__)

    if args['--verbose']:
        logging.getLogger().setLevel(logging.DEBUG)

    with open(args['--topo'], 'r') as f:
        topo = yaml.load(f)

    ensure_docker_machine()

    links = topo['links']
    nodes = [l['nodes'] for l in topo['links']]
    nodes = [item for sublist in nodes for item in sublist] # Python's way to flatten nested lists. dont' ask me why: http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
    nodes = set(nodes) # Python's way of getting unique list

    if args['up']:
        create_links(links)
        create_nodes(nodes)
        for lnk in links:
            for n in lnk['nodes']:
                link_node(lnk, n)

    if args['destroy']:
        destroy_nodes(nodes)
        destroy_links(links)

if __name__ == '__main__':
    main()
