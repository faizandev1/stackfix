"""
tests/test_analyzer.py
Tests for the pattern-matching analyzer (offline only).
"""

import pytest
from stackfix.config   import get_config
from stackfix.core     import parse, Analyzer


@pytest.fixture
def offline_cfg():
    return get_config({
        "general":   {"offline": True, "max_results": 10, "confidence_cutoff": 0.1},
        "providers": {"stackoverflow": False, "github_issues": False, "local_patterns": True},
    })


def analyze(text, cfg):
    error = parse(text)
    return Analyzer(cfg).analyze(error)


# ─────────────────────────────────────────────────────────────────────────────

def test_module_not_found_returns_fix(offline_cfg):
    results = analyze("ModuleNotFoundError: No module named 'requests'", offline_cfg)
    assert len(results) > 0


def test_module_not_found_pip_command(offline_cfg):
    results = analyze("ModuleNotFoundError: No module named 'flask'", offline_cfg)
    assert any("pip install" in (r.fix_code or "") for r in results)


def test_zero_division_confidence(offline_cfg):
    results = analyze("ZeroDivisionError: division by zero", offline_cfg)
    assert any(r.confidence >= 0.90 for r in results)


def test_key_error_fix(offline_cfg):
    results = analyze("KeyError: 'user_id'", offline_cfg)
    assert len(results) > 0


def test_bash_cmd_not_found(offline_cfg):
    results = analyze("git: command not found", offline_cfg)
    assert len(results) > 0
    assert any("install" in (r.fix_code or "").lower() for r in results)


def test_docker_daemon_fix(offline_cfg):
    results = analyze("Cannot connect to the Docker daemon", offline_cfg)
    assert len(results) > 0


def test_results_sorted_by_confidence(offline_cfg):
    results = analyze("ModuleNotFoundError: No module named 'numpy'", offline_cfg)
    confs = [r.confidence for r in results]
    assert confs == sorted(confs, reverse=True)


def test_max_results_respected(offline_cfg):
    results = analyze("ModuleNotFoundError: No module named 'anything'", offline_cfg)
    assert len(results) <= offline_cfg.get("general", "max_results", default=5)


def test_port_in_use_fix(offline_cfg):
    results = analyze("OSError: [Errno 98] Address already in use", offline_cfg)
    assert any("port" in r.title.lower() or "address" in r.title.lower() for r in results)


def test_recursion_error_fix(offline_cfg):
    results = analyze("RecursionError: maximum recursion depth exceeded", offline_cfg)
    assert len(results) > 0
    assert any("recursion" in r.title.lower() for r in results)


def test_unicode_decode_fix(offline_cfg):
    results = analyze("UnicodeDecodeError: 'utf-8' codec can't decode byte", offline_cfg)
    assert len(results) > 0


def test_generic_error_no_crash(offline_cfg):
    # Should not raise, just return (possibly empty) results
    results = analyze("something completely unrecognised 1234xyz", offline_cfg)
    assert isinstance(results, list)
