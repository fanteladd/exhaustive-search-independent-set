#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from typing import Hashable, List, Sequence, Tuple

import networkx as nx

from .greedy_is import greedyIS
from .utils import generate_graph_from_file, isIndependentSet, write_independent_set_to_file

Subproblem = Tuple[List[Hashable], List[Hashable]]


def expandProblem(P: Subproblem, G: nx.Graph) -> list[Subproblem]:
    P2 = (P[0][1:], P[1][:])
    candidate = P[0][0]
    for nodo in list(G.neighbors(candidate)):
        if nodo in P[0]:
            P[0].remove(nodo)
    P1 = (P[0][1:], P[1][:])
    P1[1].append(candidate)
    return [P1, P2]


def get_max_is_branchAndBound(G: nx.Graph) -> list[Hashable]:
    """
    Exaustive search algorithm
    """
    if G.number_of_nodes() == 0:
        return []
    S = [(list(G.nodes), [])]
    bestSoFar = greedyIS(G)
    while len(S) != 0:
        problem = S.pop()
        subProblems = expandProblem(problem, G)
        for prob in subProblems:
            newsol = prob[0] + prob[1]
            if isIndependentSet(G, prob[0]):
                if len(bestSoFar) < len(newsol):
                    bestSoFar = newsol
            elif len(bestSoFar) < len(newsol):
                S.append(prob)
    return bestSoFar


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Exact branch-and-bound independent set solver.")
    parser.add_argument("input", help="input graph file (n m header + edge list)")
    parser.add_argument("--output", default="output.txt", help="output file (default: output.txt)")
    args = parser.parse_args(argv)

    G, n, m = generate_graph_from_file(args.input)
    write_independent_set_to_file(get_max_is_branchAndBound(G), fname=args.output)


if __name__ == "__main__":
    main(sys.argv[1:])
