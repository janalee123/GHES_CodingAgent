"""Integration tests for session management."""


def test_session_creation():
    """Verify sessions can be created with valid config."""
    config = {"model": "gpt-4.1", "timeout": 30}
    assert config["model"] == "gpt-4.1"
    assert config["timeout"] == 30


def test_session_cleanup_removes_stale():
    """Verify stale sessions are cleaned up after TTL expires."""
    sessions = [
        {"id": "abc123", "age_hours": 25, "active": False},
        {"id": "def456", "age_hours": 2, "active": True},
    ]
    stale = [s for s in sessions if s["age_hours"] > 24 and not s["active"]]
    # BUG: Expected 1 stale session but asserting 2
    assert len(stale) == 2, f"Expected 2 stale sessions, got {len(stale)}"


def test_session_token_refresh():
    """Verify token refresh happens before expiry."""
    token_expiry_minutes = 5
    refresh_threshold = 10  # Should refresh when < 10 min remaining
    # BUG: Logic is inverted - this should be True but asserts False
    needs_refresh = token_expiry_minutes < refresh_threshold
    assert needs_refresh is False, "Token should not need refresh yet"
