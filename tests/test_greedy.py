import networkx as nx

from mis.greedy_is import greedyIS
from mis.utils import isIndependentSet


def test_path_graph_returns_independent_set_of_size_two():
    G = nx.path_graph(4)  # 0-1-2-3
    S = greedyIS(G)
    assert len(S) == 2
    assert isIndependentSet(G, S)


def test_random_graphs_always_valid_and_nonempty():
    for seed in range(5):
        for n in (5, 15, 30):
            for p in (0.1, 0.3, 0.6, 0.9):
                G = nx.gnp_random_graph(n, p, seed=seed)
                S = greedyIS(G)
                assert isIndependentSet(G, S)
                assert len(S) > 0


def test_empty_graph_returns_empty_list():
    G = nx.Graph()
    assert greedyIS(G) == []
