#!/usr/bin/env python3
"""
Faster exact branch-and-bound solver for the maximum independent set.

Same optimum as exhaustive_search_is.py, sped up by bitmask subproblems,
a matching-based upper bound, max-degree branching, and forced-move
reductions for degree-0/1 vertices.
"""

from __future__ import annotations

import argparse
import sys
from typing import Hashable, Iterator, Sequence

import networkx as nx

from .greedy_is_fast import greedyIS_fast
from .utils import generate_graph_from_file, write_independent_set_to_file


def _popcount(mask: int) -> int:
    return bin(mask).count("1")


def _iter_bits(mask: int) -> Iterator[int]:
    while mask:
        low = mask & (-mask)
        yield low.bit_length() - 1
        mask ^= low


def _apply_reductions(adj: list[int], free: int, chosen: int) -> tuple[int, int]:
    """Forces degree-0/1 free vertices into the solution — always safe (MIS reduction rules)."""
    changed = True
    while changed and free:
        changed = False
        for v in _iter_bits(free):
            neighbors_in_free = adj[v] & free
            deg = _popcount(neighbors_in_free)
            if deg == 0:
                free &= ~(1 << v)
                chosen |= 1 << v
                changed = True
                break
            if deg == 1:
                u = neighbors_in_free.bit_length() - 1
                free &= ~(1 << v) & ~(1 << u)
                chosen |= 1 << v
                changed = True
                break
    return free, chosen


def _max_degree_free_vertex(adj: list[int], free: int) -> int:
    best_v, best_deg = -1, -1
    for v in _iter_bits(free):
        deg = _popcount(adj[v] & free)
        if deg > best_deg:
            best_v, best_deg = v, deg
    return best_v


def _greedy_matching_size(adj: list[int], free: int) -> int:
    remaining = free
    matched = 0
    while remaining:
        low = remaining & (-remaining)
        u = low.bit_length() - 1
        remaining &= ~low
        candidates = adj[u] & remaining
        if candidates:
            low2 = candidates & (-candidates)
            remaining &= ~low2
            matched += 1
    return matched


def get_max_is_branchAndBound_fast(G: nx.Graph) -> list[Hashable]:
    """Same optimum as get_max_is_branchAndBound, just faster."""
    if G.number_of_nodes() == 0:
        return []

    nodes = list(G.nodes)
    n = len(nodes)
    index_of = {node: i for i, node in enumerate(nodes)}
    adj = [0] * n
    for u, v in G.edges:
        if u == v:
            continue
        iu, iv = index_of[u], index_of[v]
        adj[iu] |= 1 << iv
        adj[iv] |= 1 << iu

    full_mask = (1 << n) - 1
    best_mask = 0
    for node in greedyIS_fast(G):
        best_mask |= 1 << index_of[node]

    stack = [(full_mask, 0)]
    while stack:
        free, chosen = stack.pop()
        free, chosen = _apply_reductions(adj, free, chosen)

        if free == 0:
            if _popcount(chosen) > _popcount(best_mask):
                best_mask = chosen
            continue

        bound = _popcount(chosen) + _popcount(free) - _greedy_matching_size(adj, free)
        if bound <= _popcount(best_mask):
            continue

        v = _max_degree_free_vertex(adj, free)
        stack.append((free & ~(1 << v), chosen))
        stack.append((free & ~adj[v] & ~(1 << v), chosen | (1 << v)))

    return [nodes[i] for i in _iter_bits(best_mask)]


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Fast exact branch-and-bound independent set solver.")
    parser.add_argument("input", help="input graph file (n m header + edge list)")
    parser.add_argument("--output", default="output.txt", help="output file (default: output.txt)")
    args = parser.parse_args(argv)

    G, n, m = generate_graph_from_file(args.input)
    write_independent_set_to_file(get_max_is_branchAndBound_fast(G), fname=args.output)


if __name__ == "__main__":
    main(sys.argv[1:])
