#!/usr/bin/python3
"""
Usage:
    stupid.py render <format> <file>
    stupid.py dot
    stupid.py (-h | --help)

Options:
    -h --help     Show this screen.
    -v --version  Show version.

"""

from docopt import docopt
from graphviz import Digraph
import re
import sys

NODE_REGEXP = '(-+)>\s*(.*)'


class Node:
    def __init__(self, i, level, label):
        self.id = i
        self.level = level
        self.label = label

    def add_to_dot(self, dot):
        dot.node(str(self.id), self.label)


class Parser:
    def __init__(self, source):
        self.source = source
        self.dot = Digraph()

    def set_graph_attrs(self, **kwargs):
        self.dot.attr('graph', kwargs)

    def set_node_attrs(self, **kwargs):
        self.dot.attr('node', kwargs)

    def convert_to_dot(self):
        i = 0
        currents = {}

        for line in self.source.split('\n'):
            match = re.match(NODE_REGEXP, line)
            if match:
                level = len(match.group(1)) - 1
                label = match.group(2).rstrip()
                if level != 0 and not level - 1 in currents:
                    continue
                current = Node(i, level, label)
                i += 1
                current.add_to_dot(self.dot)
                currents[level] = current

                if level > 0:
                    parent = currents[level - 1]
                    self.dot.edge(str(parent.id), str(current.id))

        return self.dot

    def convert_to_source(self):
        return self.convert_to_dot().source


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Stupid 0.0.1')
    source = sys.stdin.read()
    parser = Parser(source)
    dot = parser.convert_to_dot()

    if arguments['render']:
        try:
            dot.format = arguments['<format>']
        except ValueError as e:
            sys.stderr.write(str(e) + '\n')
            sys.exit(1)
        dot.render(filename=arguments['<file>'], cleanup=True)

    elif arguments['dot']:
        print(dot.source)
