"""Shared pytest fixtures."""
import pytest

@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    """Block all outgoing network calls during tests."""
    import socket

    def guard(*args, **kwargs):
        raise ConnectionError("Network access is disabled in tests")

    monkeypatch.setattr(socket, "getaddrinfo", guard)
