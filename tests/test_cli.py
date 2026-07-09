import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "src"


def _write_input(tmp_path):
    input_path = tmp_path / "input.txt"
    input_path.write_text("4 3\n0 1\n1 2\n2 3\n")
    return input_path


def _run_cli(module_name, input_path, cwd):
    env = dict(os.environ, PYTHONPATH=str(SRC))
    return subprocess.run(
        [sys.executable, "-m", f"mis.{module_name}", str(input_path)],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
    )


def _assert_valid_output(tmp_path, result):
    assert result.returncode == 0, result.stderr
    output_path = tmp_path / "output.txt"
    lines = output_path.read_text().splitlines()
    assert int(lines[0]) == len(lines[1:])


def test_exact_cli_produces_valid_output(tmp_path):
    input_path = _write_input(tmp_path)
    result = _run_cli("exhaustive_search_is", input_path, tmp_path)
    _assert_valid_output(tmp_path, result)


def test_greedy_cli_produces_valid_output(tmp_path):
    input_path = _write_input(tmp_path)
    result = _run_cli("greedy_is", input_path, tmp_path)
    _assert_valid_output(tmp_path, result)


def test_exact_fast_cli_produces_valid_output(tmp_path):
    input_path = _write_input(tmp_path)
    result = _run_cli("exhaustive_search_is_fast", input_path, tmp_path)
    _assert_valid_output(tmp_path, result)


def test_greedy_fast_cli_produces_valid_output(tmp_path):
    input_path = _write_input(tmp_path)
    result = _run_cli("greedy_is_fast", input_path, tmp_path)
    _assert_valid_output(tmp_path, result)


def test_cli_respects_output_flag(tmp_path):
    input_path = _write_input(tmp_path)
    env = dict(os.environ, PYTHONPATH=str(SRC))
    result = subprocess.run(
        [sys.executable, "-m", "mis.greedy_is", str(input_path), "--output", "custom.txt"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    lines = (tmp_path / "custom.txt").read_text().splitlines()
    assert int(lines[0]) == len(lines[1:])
