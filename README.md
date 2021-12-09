# AST visualizer

The script `astvisualizer.py` contained in this repository visualizes a Python AST trees.

## Installation

First install the following requirements:
  * Python 3
  * [Graphviz](https://www.graphviz.org/download/)
  * the dependencies listed in requirements.txt (`pip install -r requirements` or `pip3 install -r requirements` depending on your OS)

Run the script `astvisualizer.py`. It accepts the input on stdin. Alternatively you might specify a file name as first parameter.

## Usage

By default `astvisualizer.py` reads the Python code from stdin.

If you only want to visualize a short snippet you can also pass it directly on the command line, f.e. `astvisualizer.py "print(3/2)"`.

If you want to visualize an existing Python source code file, pass the file name using the `-f` switch, f.e. `astvisualizer.py -f test.py`.

## Development

Resources I (@jmanuel1) found useful while working on this code:
- http://www.graphviz.org/doc/info/attrs.html
- http://graphs.grevian.org/example#example-6
- https://stackoverflow.com/questions/2012036/graphviz-how-to-connect-subgraphs
- https://renenyffenegger.ch/notes/tools/Graphviz/elems/subgraph/index
- https://graphviz.org/documentation/
- https://gitlab.com/graphviz/graphviz/-/issues/1348
- https://gitlab.com/graphviz/graphviz/-/issues/68
- https://graphviz.readthedocs.io/en/stable/manual.html#subgraphs-clusters

## Acknowledgements

This repository is a fork of
https://github.com/pombredanne/python-ast-visualizer.
