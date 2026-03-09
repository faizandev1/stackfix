"""
tests/test_parser.py
Tests for the multi-language error parser.
"""

import pytest
from stackfix.core.parser import parse, Language


# ─────────────────────────────────────────────────────────────────────────────
# PYTHON
# ─────────────────────────────────────────────────────────────────────────────

PYTHON_MODULE_ERROR = """\
Traceback (most recent call last):
  File "app.py", line 1, in <module>
    import requests
ModuleNotFoundError: No module named 'requests'
"""

PYTHON_TYPE_ERROR = """\
Traceback (most recent call last):
  File "script.py", line 5, in compute
    result = value + "hello"
TypeError: unsupported operand type(s) for +: 'int' and 'str'
"""

PYTHON_KEY_ERROR = """\
Traceback (most recent call last):
  File "handler.py", line 12, in process
    user = data['user']
KeyError: 'user'
"""

PYTHON_ZERO_DIV = """\
Traceback (most recent call last):
  File "calc.py", line 3, in divide
    return a / b
ZeroDivisionError: division by zero
"""

PYTHON_RECURSION = """\
Traceback (most recent call last):
  File "tree.py", line 8, in walk
    walk(node.left)
  [Previous line repeated 996 more times]
RecursionError: maximum recursion depth exceeded
"""

PYTHON_FILE_NOT_FOUND = """\
Traceback (most recent call last):
  File "loader.py", line 4, in load
    with open('/etc/missing.conf') as f:
FileNotFoundError: [Errno 2] No such file or directory: '/etc/missing.conf'
"""


def test_module_not_found_language():
    r = parse(PYTHON_MODULE_ERROR)
    assert r.language == Language.PYTHON


def test_module_not_found_type():
    r = parse(PYTHON_MODULE_ERROR)
    assert r.error_type == "ModuleNotFoundError"


def test_module_not_found_message():
    r = parse(PYTHON_MODULE_ERROR)
    assert "requests" in r.message


def test_module_not_found_frames():
    r = parse(PYTHON_MODULE_ERROR)
    assert len(r.frames) >= 1
    assert "app.py" in r.frames[0].filename


def test_type_error():
    r = parse(PYTHON_TYPE_ERROR)
    assert r.language   == Language.PYTHON
    assert r.error_type == "TypeError"
    assert r.frames[-1].function == "compute"


def test_key_error():
    r = parse(PYTHON_KEY_ERROR)
    assert r.error_type == "KeyError"
    assert "user" in (r.message or "")


def test_zero_division():
    r = parse(PYTHON_ZERO_DIV)
    assert r.error_type == "ZeroDivisionError"


def test_recursion_error():
    r = parse(PYTHON_RECURSION)
    assert r.error_type == "RecursionError"


def test_file_not_found():
    r = parse(PYTHON_FILE_NOT_FOUND)
    assert r.error_type == "FileNotFoundError"
    assert r.frames[-1].filename == "loader.py"


# ─────────────────────────────────────────────────────────────────────────────
# JAVASCRIPT
# ─────────────────────────────────────────────────────────────────────────────

JS_NULL_ERROR = """\
TypeError: Cannot read properties of null (reading 'name')
    at getUser (app.js:12:10)
    at handler (server.js:34:5)
"""

JS_MODULE_ERROR = """\
Error: Cannot find module 'express'
Require stack:
    at server.js:1
"""

JS_HEAP_ERROR = """\
FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory
"""


def test_js_type_error():
    r = parse(JS_NULL_ERROR)
    assert r.language   == Language.JAVASCRIPT
    assert r.error_type == "TypeError"
    assert len(r.frames) >= 1


def test_js_module_not_found():
    r = parse(JS_MODULE_ERROR)
    assert r.language   == Language.JAVASCRIPT
    assert r.error_type == "Error"
    assert "express" in (r.message or "")


def test_js_heap_memory():
    r = parse(JS_HEAP_ERROR)
    # Falls back to generic, but should not crash
    assert r is not None


# ─────────────────────────────────────────────────────────────────────────────
# BASH
# ─────────────────────────────────────────────────────────────────────────────

BASH_CMD_NOT_FOUND = "git: command not found"
BASH_PERM_DENIED   = "bash: ./deploy.sh: Permission denied"
BASH_NO_FILE       = "ls: cannot access '/missing': No such file or directory"


def test_bash_command_not_found():
    r = parse(BASH_CMD_NOT_FOUND)
    assert r.language   == Language.BASH
    assert r.error_type == "CommandNotFound"
    assert r.command    == "git"


def test_bash_permission_denied():
    r = parse(BASH_PERM_DENIED)
    assert r.language == Language.BASH


def test_bash_no_such_file():
    r = parse(BASH_NO_FILE)
    assert r.language == Language.BASH


# ─────────────────────────────────────────────────────────────────────────────
# DOCKER
# ─────────────────────────────────────────────────────────────────────────────

DOCKER_IMAGE_NOT_FOUND = """\
Error response from daemon: manifest for myimage:notexist not found: \
manifest unknown: manifest unknown
"""

DOCKER_DAEMON = "Cannot connect to the Docker daemon at unix:///var/run/docker.sock"


def test_docker_image_not_found():
    r = parse(DOCKER_IMAGE_NOT_FOUND)
    assert r.language   == Language.DOCKER
    assert r.error_type == "DockerError"


def test_docker_daemon():
    r = parse(DOCKER_DAEMON)
    assert r.language == Language.DOCKER


# ─────────────────────────────────────────────────────────────────────────────
# ParsedError helpers
# ─────────────────────────────────────────────────────────────────────────────

def test_short_message_truncates():
    r = parse(PYTHON_MODULE_ERROR)
    assert len(r.short_message) <= 200


def test_last_frame():
    r = parse(PYTHON_TYPE_ERROR)
    assert r.last_frame is not None
    assert r.last_frame.filename == "script.py"


def test_generic_fallback():
    r = parse("something went totally wrong somehow")
    assert r.language == Language.GENERIC
    assert r is not None
