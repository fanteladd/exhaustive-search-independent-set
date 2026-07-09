#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from typing import Hashable, Sequence

import networkx as nx

from .utils import degMinNode, generate_graph_from_file, write_independent_set_to_file


def greedyIS(graph: nx.Graph) -> list[Hashable]:
    """
    Non-optimal greedy algorithm.
    """
    G = graph.copy()
    S = []
    while G.number_of_nodes() != 0:
        v = degMinNode(G)
        S.append(v)
        G.remove_nodes_from(list(G.neighbors(v)) + [v])
    return S


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Greedy independent set heuristic.")
    parser.add_argument("input", help="input graph file (n m header + edge list)")
    parser.add_argument("--output", default="output.txt", help="output file (default: output.txt)")
    args = parser.parse_args(argv)

    G, n, m = generate_graph_from_file(args.input)
    write_independent_set_to_file(greedyIS(G), fname=args.output)


if __name__ == "__main__":
    main(sys.argv[1:])
