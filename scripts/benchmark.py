#!/usr/bin/env python3
"""
Benchmarks all four solvers on seeded random graphs: sizes, approximation
ratio, and wall time — so the fast variants' gains are measured, not assumed.

Usage: python3 scripts/benchmark.py (src/ on PYTHONPATH, or after `pip install -e .`)
"""

from __future__ import annotations

import time
from typing import Callable

import networkx as nx

from mis.exhaustive_search_is import get_max_is_branchAndBound
from mis.exhaustive_search_is_fast import get_max_is_branchAndBound_fast
from mis.greedy_is import greedyIS
from mis.greedy_is_fast import greedyIS_fast

# Exact grid stays small (exponential worst case); greedy grid scales larger.
EXACT_SIZES = (20, 30, 40, 50)
GREEDY_SIZES = (30, 100, 300, 1000)
MAX_FEASIBLE_EXACT_N = 50
DENSITIES = (0.1, 0.2, 0.3)
SEEDS = (0, 1, 2)


def _time_solver(solver: Callable[[nx.Graph], list], G: nx.Graph) -> tuple[int, float]:
    t0 = time.perf_counter()
    result = solver(G)
    elapsed = time.perf_counter() - t0
    return len(result), elapsed


def _print_table(title: str, headers: list[str], rows: list[list[str]]) -> None:
    print(f"\n{title}")
    widths = [max(len(h), *(len(r[i]) for r in rows)) for i, h in enumerate(headers)]
    print("  ".join(h.ljust(w) for h, w in zip(headers, widths)))
    print("  ".join("-" * w for w in widths))
    for row in rows:
        print("  ".join(c.ljust(w) for c, w in zip(row, widths)))


def benchmark_exact() -> None:
    rows = []
    for n in EXACT_SIZES:
        for p in DENSITIES:
            for seed in SEEDS:
                G = nx.gnp_random_graph(n, p, seed=seed)
                slow_size, slow_time = _time_solver(get_max_is_branchAndBound, G)
                fast_size, fast_time = _time_solver(get_max_is_branchAndBound_fast, G)
                speedup = slow_time / fast_time if fast_time > 0 else float("inf")
                rows.append(
                    [
                        str(n),
                        f"{p:.2f}",
                        str(seed),
                        str(slow_size),
                        str(fast_size),
                        f"{slow_time * 1000:.1f}",
                        f"{fast_time * 1000:.1f}",
                        f"{speedup:.1f}x",
                    ]
                )
    _print_table(
        "Exact solvers: exhaustive_search_is vs exhaustive_search_is_fast",
        ["n", "p", "seed", "slow_size", "fast_size", "slow_ms", "fast_ms", "speedup"],
        rows,
    )


def benchmark_greedy() -> None:
    rows = []
    for n in GREEDY_SIZES:
        for p in DENSITIES:
            for seed in SEEDS:
                G = nx.gnp_random_graph(n, p, seed=seed)
                if n <= MAX_FEASIBLE_EXACT_N:
                    exact_size, _ = _time_solver(get_max_is_branchAndBound_fast, G)
                else:
                    exact_size = None
                greedy_size, greedy_time = _time_solver(greedyIS, G)
                fast_size, fast_time = _time_solver(greedyIS_fast, G)
                ratio = f"{greedy_size / exact_size:.2f}" if exact_size else "n/a"
                rows.append(
                    [
                        str(n),
                        f"{p:.2f}",
                        str(seed),
                        str(greedy_size),
                        str(fast_size),
                        f"{greedy_time * 1000:.2f}",
                        f"{fast_time * 1000:.2f}",
                        ratio,
                    ]
                )
    _print_table(
        "Greedy heuristics: greedy_is vs greedy_is_fast (approx. ratio vs optimum where feasible)",
        ["n", "p", "seed", "greedy_size", "fast_size", "greedy_ms", "fast_ms", "approx_ratio"],
        rows,
    )


def main() -> None:
    benchmark_exact()
    benchmark_greedy()


if __name__ == "__main__":
    main()
