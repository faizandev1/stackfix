"""Shared pytest fixtures — block network so tests are fully offline."""
import pytest


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    """
    Prevent any real network calls during the test suite.
    Providers that need network will simply return [] which is correct behaviour.
    """
    import socket
    original = socket.getaddrinfo

    def guard(host, *args, **kwargs):
        # Allow localhost lookups (needed by some stdlib internals)
        if host in ("localhost", "127.0.0.1", "::1"):
            return original(host, *args, **kwargs)
        raise OSError(f"Network access blocked in tests (tried to reach: {host})")

    monkeypatch.setattr(socket, "getaddrinfo", guard)
