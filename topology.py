import yaml
import uuid
import string
import sys

class TopologySpecError(Exception):
    pass

class Topology:

    def __init__(self, topo_yaml):
        with open(topo_yaml, 'r') as f:
            self.spec = yaml.load(f)

        # Figure out how many nodes in this topo
        link_spec = self.spec['links']
        node_list = [l.get('nodes', []) for l in link_spec]
        flattened_node_list = [item for sublist in node_list for item in sublist] # Python's way to flatten nested lists. dont' ask me why: http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
        uniq_nodes = set(flattened_node_list) # Python's way of getting unique list
        self.nodes = [Node(n) for n in uniq_nodes]

        all_link_names = [l['name'] for l in link_spec]
        if len(set(all_link_names)) != len(all_link_names):
            raise TopologySpecError('Duplicate link names in ' + topo_yaml)

        self.links = []
        for link_dict in link_spec:
            ajacent_nodes = [n for n in self.nodes if n.name in link_dict.get('nodes', [])]
            self.links.append(Link(link_dict, ajacent_nodes))

    def node_by_name(self, name):
        matches = [n for n in self.nodes if n.name == name]
        return matches[0] if matches else None

    def draw(self):
        from termcolor import colored, cprint
        print('')
        cprint('Link', 'green', end='')
        sys.stdout.write(7*' ')
        cprint('Network Interface', 'yellow', end='')
        sys.stdout.write(5*' ')
        cprint('Node', 'red')
        print(50*'-' + '\n')
        for link in self.links:
            cprint(link.name, 'green')
            print('|')
            for interface in link.interfaces:
                print('|')
                sys.stdout.write(12*'-' + '<')
                cprint(interface.name, 'yellow', end='')
                sys.stdout.write('>' + 8*'-')
                cprint(interface.node.name, 'red')
            print('')

class Link:

    def __init__(self, data_dict, ajacent_nodes):
        self.name = data_dict['name']
        self.bridge_name = 'YANS-' + self.name
        self.interfaces = [Interface(self, node) for node in ajacent_nodes]


class Interface:

    def __init__(self, link, node):
        self.link = link
        self.node = node
        self.name = 'yans' + random_id()
        self.peer_name = self.name + '-p'
        self.node.interfaces.append(self)


class Node:

    def __init__(self, name):
        self.name = name
        self.container_name = 'YANS-' + self.name
        self.interfaces = []


def random_id(size=6, chars=string.letters + string.digits):
    import random
    return ''.join(random.choice(chars) for _ in range(size))

