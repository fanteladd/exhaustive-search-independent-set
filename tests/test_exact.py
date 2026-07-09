from itertools import combinations

import networkx as nx

from mis.exhaustive_search_is import get_max_is_branchAndBound
from mis.utils import isIndependentSet


def brute_force_optimum(G):
    nodes = list(G.nodes)
    for k in range(len(nodes), -1, -1):
        for combo in combinations(nodes, k):
            if isIndependentSet(G, combo):
                return k
    return 0


def test_optimality_against_brute_force():
    for seed in range(30):
        n = seed % 9 + 1
        p = 0.2 + (seed % 5) * 0.15
        G = nx.gnp_random_graph(n, p, seed=seed)
        exact = get_max_is_branchAndBound(G)
        assert isIndependentSet(G, exact)
        assert len(exact) == brute_force_optimum(G)


def test_validity_random_graphs():
    for seed in range(10):
        G = nx.gnp_random_graph(8, 0.5, seed=seed)
        S = get_max_is_branchAndBound(G)
        assert isIndependentSet(G, S)


def test_empty_graph_returns_empty_list():
    assert get_max_is_branchAndBound(nx.Graph()) == []


def test_single_node_returns_that_node():
    G = nx.Graph()
    G.add_node(0)
    assert get_max_is_branchAndBound(G) == [0]


def test_complete_graph_k5_returns_size_one():
    G = nx.complete_graph(5)
    assert len(get_max_is_branchAndBound(G)) == 1


def test_no_edges_graph_returns_all_nodes():
    G = nx.Graph()
    G.add_nodes_from(range(6))
    assert len(get_max_is_branchAndBound(G)) == 6
