import networkx as nx

from mis.utils import (
    generate_graph_from_file,
    isIndependentSet,
    random_graph_generator,
    write_independent_set_to_file,
)


def test_parser_readme_example(tmp_path):
    fpath = tmp_path / "input.txt"
    fpath.write_text("4 3\n0 1\n1 2\n2 3\n")
    G, n, m = generate_graph_from_file(str(fpath))
    assert isinstance(n, int)
    assert isinstance(m, int)
    assert n == 4
    assert m == 3
    assert sorted(G.nodes) == [0, 1, 2, 3]
    assert sorted(G.edges) == [(0, 1), (1, 2), (2, 3)]


def test_parser_preserves_isolated_node(tmp_path):
    fpath = tmp_path / "input.txt"
    fpath.write_text("3 1\n0 1\n")
    G, n, m = generate_graph_from_file(str(fpath))
    assert n == 3
    assert G.number_of_nodes() == 3
    assert 2 in G.nodes


def test_parser_trailing_blank_line_does_not_raise(tmp_path):
    fpath = tmp_path / "input.txt"
    fpath.write_text("4 3\n0 1\n1 2\n2 3\n\n")
    G, n, m = generate_graph_from_file(str(fpath))
    assert n == 4
    assert m == 3
    assert G.number_of_nodes() == 4


def test_isIndependentSet_true_case():
    G = nx.path_graph(4)  # edges 0-1, 1-2, 2-3
    assert isIndependentSet(G, [0, 2]) is True


def test_isIndependentSet_false_case_adjacent_pair():
    G = nx.path_graph(4)
    assert isIndependentSet(G, [0, 1]) is False


def test_isIndependentSet_empty_list_is_true():
    G = nx.path_graph(4)
    assert isIndependentSet(G, []) is True


def test_write_independent_set_to_file(tmp_path):
    fpath = tmp_path / "output.txt"
    write_independent_set_to_file([3, 1, 4], fname=str(fpath))
    lines = fpath.read_text().splitlines()
    assert lines[0] == "3"
    assert lines[1:] == ["3", "1", "4"]


def test_random_graph_generator_writes_parseable_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    random_graph_generator(10, 0.5)
    G, n, m = generate_graph_from_file(str(tmp_path / "input.txt"))
    assert n == 10
    assert G.number_of_nodes() == 10
