#!/usr/bin/env python3

from __future__ import annotations

from typing import Collection, Hashable, Iterable

import networkx as nx


def random_graph_generator(n: int, p: float, fname: str = "input.txt", seed: int | None = None) -> nx.Graph:
    """
    Generates a random G(n, p) graph, writes it to fname in the project's
    edge-list format, and returns the graph.
    """
    G = nx.gnp_random_graph(n, p, seed=seed, directed=False)
    with open(fname, "w") as f:
        f.write(f"{len(list(G.nodes))} {len(list(G.edges))}\n")
        for e in G.edges:
            f.write(f"{e[0]} {e[1]}\n")
    return G


def generate_graph_from_file(fname: str = "input.txt") -> tuple[nx.Graph, int, int]:
    """
    Given an input file, it returns a graph G with n nodes and m edges.
    """
    G = nx.Graph()

    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    n, m = (int(x) for x in lines[0].split(" "))
    G.add_nodes_from(range(n))

    for line in lines[1:]:
        u, v = (int(x) for x in line.split(" "))
        G.add_edge(u, v)

    return G, n, m


def isIndependentSet(G: nx.Graph, nodelist: Iterable[Hashable]) -> bool:
    """
    Given a graph G and a list of nodes nodelist, it checks if
    nodelist is an independent set for G.
    """
    node_set = set(nodelist)
    for u in node_set:
        for v in G.neighbors(u):
            if v in node_set:
                return False
    return True


def write_independent_set_to_file(iset: Collection[Hashable], fname: str = "output.txt") -> None:
    """
    Given a list of nodes, it writes the list of nodes to a file.
    """
    with open(fname, "w") as f:
        f.write(str(len(iset)) + "\n")
        for node in iset:
            f.write(str(node) + "\n")


def degMinNode(G: nx.Graph) -> Hashable:
    """
    Given a graph G, it returns the node of G with the minimum degree.
    """
    return min(G.nodes, key=G.degree)
