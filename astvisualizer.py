#!/usr/bin/python3
import ast
import graphviz as gv
import subprocess
import numbers
import re
from uuid import uuid4 as uuid
import optparse
import sys

def main(args):
    parser = optparse.OptionParser(usage="astvisualizer.py [options] [string]")
    parser.add_option("-f", "--file", action="store",
                      help="Read a code snippet from the specified file")
    parser.add_option("-l", "--label", action="store",
                      help="The label for the visualization")

    options, args = parser.parse_args(args)
    if options.file:
        with open(options.file) as instream:
            code = instream.read()
        label = options.file
    elif len(args) == 2:
        code = args[1]
        label = "<code read from command line parameter>"
    else:
        print("Expecting Python code on stdin...")
        code = sys.stdin.read()
        label = "<code read from stdin>"
    if options.label:
        label = options.label

    code_ast = ast.parse(code)
    transformed_ast = transform_ast(code_ast)

    renderer = GraphRenderer()
    renderer.render(transformed_ast, label=label)


def transform_ast(code_ast):
    if isinstance(code_ast, ast.AST):
        node = {to_camelcase(k): transform_ast(getattr(code_ast, k)) for k in code_ast._fields}
        node['node_type'] = code_ast.__class__.__name__
        return node
    elif isinstance(code_ast, list):
        return [transform_ast(el) for el in code_ast]
    else:
        return code_ast


def to_camelcase(string):
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', string).lower()


class GraphRenderer:
    """
    this class is capable of rendering data structures consisting of
    dicts and lists as a graph using graphviz
    """

    graphattrs = {
        'labelloc': 't',
        'fontcolor': 'black',
        'bgcolor': 'white',
        'margin': '0',
        'fontname': 'Helvetica',
        'fontsize': '16',
        'ranksep': '1',
        'nodesep': '2'
    }

    nodeattrs = {
        'color': 'black',
        'fontcolor': 'black',
        'style': 'filled',
        'fillcolor': 'white',
        'fontname': 'Helvetica',
        'fontsize': '16',
        'shape': 'rect',
        'fixedsize': 'false',
        'width': str(120/72),
        'height': str(60/72),
    }

    edgeattrs = {
        'color': 'black',
        'fontcolor': 'black',
        'labeldistance': '4',
        'labelangle': '0',
        'bgcolor': 'white',
        'fontname': 'Helvetica',
        'fontsize': '16'
    }

    _graph = None
    _rendered_nodes = None


    @staticmethod
    def _escape_dot_label(str):
        return str.replace("\\", "\\\\").replace("|", "\\|").replace("<", "\\<").replace(">", "\\>")

    @staticmethod
    def _table(str):
        return '< <table bgcolor="white" border="0"><tr><td>' + str + '</td></tr></table> >'

    @staticmethod
    def _italic(str):
        return '<i>' + str + '</i>'


    def _render_node(self, node):
        if isinstance(node, (str, numbers.Number)) or node is None:
            node_id = uuid()
        else:
            node_id = id(node)
        node_id = str(node_id)

        if node_id not in self._rendered_nodes:
            self._rendered_nodes.add(node_id)
            if isinstance(node, dict):
                self._render_dict(node, node_id)
            elif isinstance(node, list):
                self._render_list(node, node_id)
            else:
                # do nothing
                pass

        return node_id


    def _render_dict(self, node, node_id):
        label = node.get("node_type", "[dict]")
        for key, value in node.items():
            if key != 'node_type' and not isinstance(value, (list, dict)):
                label += '\n' + key + ' = ' + repr(value)
        self._graph.node(node_id, label=label)
        for key, value in node.items():
            if key == "node_type" or not isinstance(value, (list, dict)):
                continue
            child_node_id = self._render_node(value)
            self._graph.edge(node_id, child_node_id, headlabel=self._table(self._escape_dot_label(key)))


    def _render_list(self, node, node_id):
        label = self._italic("List")
        if not node:
            with self._graph.subgraph(name='cluster_' + str(uuid()), graph_attr={'label': '(Empty)', 'border': '0', 'labelloc': 'b', 'pencolor': 'white'}) as c:
                c.node(node_id, label='<' + label + '>', shape='circle', width=str(50/72))
        else:
            self._graph.node(node_id, label='<' + label + '>', shape='circle', width=str(50/72))

            for idx, value in enumerate(node):
                child_node_id = self._render_node(value)
                self._graph.edge(node_id, child_node_id, headlabel=self._table(self._escape_dot_label(str(idx))))


    def render(self, data, *, label=None):
        # create the graph
        graphattrs = self.graphattrs.copy()
        graph = gv.Digraph(graph_attr = graphattrs, node_attr = self.nodeattrs, edge_attr = self.edgeattrs)

        # recursively draw all the nodes and edges
        self._graph = graph
        self._rendered_nodes = set()
        self._render_node(data)
        self._graph = None
        self._rendered_nodes = None

        # render the graph to SVG
        result = graph.pipe(format='svg').decode('utf-8')
        print(result)


if __name__ == '__main__':
    main(sys.argv)
