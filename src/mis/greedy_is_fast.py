#!/usr/bin/env python3
"""
Greedy independent set heuristic using a degree-bucket queue.

Same strategy as greedy_is.py, but O(n + m) instead of O(n^2) since the
minimum-degree node is tracked in buckets instead of rescanned each pick.
"""

from __future__ import annotations

import argparse
import sys
from typing import Hashable, Sequence

import networkx as nx

from .utils import generate_graph_from_file, write_independent_set_to_file


def greedyIS_fast(graph: nx.Graph) -> list[Hashable]:
    """Same as greedyIS, just faster on large graphs."""
    G = graph.copy()
    if G.number_of_nodes() == 0:
        return []

    active = set(G.nodes)
    degree = {v: G.degree(v) for v in active}
    max_degree = max(degree.values(), default=0)
    buckets = [set() for _ in range(max_degree + 1)]
    for v, d in degree.items():
        buckets[d].add(v)

    solution = []
    current = 0
    while active:
        while not buckets[current]:
            current += 1
        v = buckets[current].pop()
        active.discard(v)
        solution.append(v)

        for u in list(G.neighbors(v)):
            if u not in active:
                continue
            active.discard(u)
            buckets[degree[u]].discard(u)
            for w in G.neighbors(u):
                if w in active:
                    d = degree[w]
                    buckets[d].discard(w)
                    degree[w] = d - 1
                    buckets[d - 1].add(w)
                    if d - 1 < current:
                        current = d - 1

    return solution


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Greedy independent set heuristic (degree-bucket queue).")
    parser.add_argument("input", help="input graph file (n m header + edge list)")
    parser.add_argument("--output", default="output.txt", help="output file (default: output.txt)")
    args = parser.parse_args(argv)

    G, n, m = generate_graph_from_file(args.input)
    write_independent_set_to_file(greedyIS_fast(G), fname=args.output)


if __name__ == "__main__":
    main(sys.argv[1:])
