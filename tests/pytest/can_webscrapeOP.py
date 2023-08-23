import pytest
import can_webscrape.py

@pytest.mark.parametrize("content, user_agent, expected", [
    ("""
    User-agent: *
    Disallow: /
    """, "MyWebScraperBot", False),

    ("""
    User-agent: *
    Allow: /
    """, "MyWebScraperBot", True)
])
def test_can_webscrape(content, user_agent, expected):
    result = can_webscrape(content, user_agent)
    assert result == expected

