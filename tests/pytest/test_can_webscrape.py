import requests
import pytest
from unittest.mock import patch, Mock
import _can_webscrape

class TestFetchRobotsTxt:
    
    @pytest.mark.parametrize("status_code, text, expected_result", [
        (200, "User-agent: *\nDisallow:", "User-agent: *\nDisallow:"),  # Successful fetch
        (200, "  User-agent: *\nDisallow:  ", "User-agent: *\nDisallow:"),  # Stripping whitespaces
    ])
    @patch('requests.get')
    def test_successful_fetch_robots_txt(self, mock_get, status_code, text, expected_result):
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.text = text
        mock_get.return_value = mock_response
        
        result = _can_webscrape.fetch_robots_txt("http://fake-url.com/robots.txt")
        assert result == expected_result, f"For status code {status_code} and text '{text}', expected '{expected_result}' but got '{result}'"

    @pytest.mark.parametrize("status_code, text", [
        (404, ""),
        (500, "Server Error"),
        (403, "Forbidden"),
    ])
    @patch('requests.get')
    def test_failed_fetch_robots_txt(self, mock_get, status_code, text):
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.text = text
        mock_get.return_value = mock_response
        
        with pytest.raises(Exception, match=f"Failed to fetch robots.txt from http://fake-url.com/robots.txt"):
            _can_webscrape.fetch_robots_txt("http://fake-url.com/robots.txt")
            
    @patch('requests.get')
    def test_fetch_invalid_url(self, mock_get):
        # Mock isn't strictly necessary here since we're not going to make a request.
        # However, to ensure consistency with other tests and to prevent accidental requests, I'm keeping the patch.
        invalid_urls = [
            "http://fake-url.com/",
            "http://fake-url.com/pages",
            "http://fake-url.com/robot",
            "http://fake-url.com/robots.txt.zip",
        ]
        for url in invalid_urls:
            with pytest.raises(Exception, match=f"Invalid URL '{url}'. The URL should end with 'robots.txt'"):
                _can_webscrape.fetch_robots_txt(url)

class TestSeparateRobotsTxtByGroup:
    
    def test_empty_input(self):
        input_txt = ""
        expected_output = []
        result = _can_webscrape.separate_robot_txt_by_groups(input_txt)
        assert result == expected_output, f"Expected {expected_output} but got {result}"

    def test_txt_no_newline(self):
        input_txt = "User-agent: * Disallow: /admin Disallow: /login"
        expected_output = ["User-agent: *", "Disallow: /admin", "Disallow: /login"]
        result = _can_webscrape.separate_robot_txt_by_groups(input_txt)
        assert result == expected_output, f"Expected {expected_output} but got {result}"
        
    def test_sequential_order(self):
        input_txt = "user-agent: Bot disallow: /admin Disallow: /login User-agent: * Disallow: /folders"
        expected_output = ["user-agent: Bot", "disallow: /admin", "Disallow: /login", "User-agent: *", "Disallow: /folders"]
        result = _can_webscrape.separate_robot_txt_by_groups(input_txt)
        assert result == expected_output, f"Expected {expected_output} but got {result}"
        
    def test_with_newlines(self):
        input_txt = "User-agent: *\nDisallow: /admin\nDisallow: /login"
        expected_output = ["User-agent: *", "Disallow: /admin", "Disallow: /login"]
        result = _can_webscrape.separate_robot_txt_by_groups(input_txt)
        assert result == expected_output, f"Expected {expected_output} but got {result}"
        
    def test_whitespaces(self):
        input_txt = "    User-agent: Bot    Disallow: /example   "
        expected_output = ["User-agent: Bot", "Disallow: /example"]
        result = _can_webscrape.separate_robot_txt_by_groups(input_txt)
        assert result == expected_output, f"Expected {expected_output} but got {result}"
        
    def test_multiple_newlines(self):
        input_txt = "User-agent: *\n\n\nDisallow: /admin"
        expected_output = ["User-agent: *", "Disallow: /admin"]
        result = _can_webscrape.separate_robot_txt_by_groups(input_txt)
        assert result == expected_output, f"Expected {expected_output} but got {result}"
        
    def test_directives_without_values(self):
        input_txt = "User-agent: *\nDisallow:"
        expected_output = ["User-agent: *", "Disallow:"]
        result = _can_webscrape.separate_robot_txt_by_groups(input_txt)
        assert result == expected_output, f"Expected {expected_output} but got {result}"
        
    def test_unrecognized_directives(self):
        input_txt = "# This is a comment\nUser-agent: *\nDisallow: /admin\nRandom-directive: ignore"
        expected_output = ["User-agent: *", "Disallow: /admin"]
        result = _can_webscrape.separate_robot_txt_by_groups(input_txt)
        assert result == expected_output, f"Expected {expected_output} but got {result}"

class TestFilterUserAgent:
    def test_filter_user_agent(self):
        input_txt = ['user-agent: sitebot', 'disallow: /', 'User-agent: *', 'Disallow: /favourites', 'sitemap: https://smarkets.com/sitemap.xml']
        expected_output = ['User-agent: *', 'Disallow: /favourites', 'sitemap: https://smarkets.com/sitemap.xml']
        result = _can_webscrape.filter_user_agent(input_txt)
        assert result == expected_output, f"Expected {expected_output} but got {result}"
    
    def test_multiple_user_agent_star(self):
        input_txt = ['User-agent: *', 'Disallow: /first', 'User-agent: *', 'Disallow: /second']
        expected_output = ['User-agent: *', 'Disallow: /first', 'Disallow: /second']
        result = _can_webscrape.filter_user_agent(input_txt)
        assert result == expected_output, f"Expected {expected_output} but got {result}"
    
    def test_rules_outside_user_agent(self):
        input_txt = ['Disallow: /noagent', 'User-agent: *', 'Disallow: /yesagent']
        expected_output = ['User-agent: *', 'Disallow: /yesagent']
        result = _can_webscrape.filter_user_agent(input_txt)
        assert result == expected_output, f"Expected {expected_output} but got {result}"
        
    def test_empty_input(self):
        input_txt = []
        expected_output = []
        result = _can_webscrape.filter_user_agent(input_txt)
        assert result == expected_output, f"Expected {expected_output} but got {result}"
    
    def test_additional_whitespaces(self):
        input_txt = ['User-agent: *   ', '   Disallow: /yesagent   ']
        expected_output = ['User-agent: *', 'Disallow: /yesagent']
        result = _can_webscrape.filter_user_agent(input_txt)
        assert result == expected_output, f"Expected {expected_output} but got {result}"
    
    def test_mix_of_rules(self):
        input_txt = ['User-agent: googlebot', 'Disallow: /google', 'User-agent: *', 'Disallow: /all']
        expected_output = ['User-agent: *', 'Disallow: /all']
        result = _can_webscrape.filter_user_agent(input_txt)
        assert result == expected_output, f"Expected {expected_output} but got {result}"
        
    def test_rules_after_globals(self):
        input_txt = ['User-agent: *', 'Sitemap: https://example.com/sitemap.xml', 'Disallow: /yesagent']
        expected_output = ['User-agent: *', 'Sitemap: https://example.com/sitemap.xml', 'Disallow: /yesagent']
        result = _can_webscrape.filter_user_agent(input_txt)
        assert result == expected_output, f"Expected {expected_output} but got {result}"

class TestRobotListToDict:
    def test_robot_list_to_dict(self):
        input_list = ["Disallow: /admin", "User-agent: *", "Disallow: /login", "sitemap: https://smarkets.com/sitemap.xml"]
        expected_output = {
            "Disallow": ["/admin", "/login"],
            "User-agent": ["*"],
            "sitemap" : ["https://smarkets.com/sitemap.xml"]
        }
        result = _can_webscrape.robot_list_to_dict(input_list)
        assert result == expected_output, f"Expected {expected_output}, but got {result}"
        
    def test_repetitive_keys(self):
        input_list = ["Disallow: /admin", "Disallow: /login", "Disallow: /dashboard"]
        expected_output = {
            "Disallow": ["/admin", "/login", "/dashboard"]
        }
        result = _can_webscrape.robot_list_to_dict(input_list)
        assert result == expected_output, f"Expected {expected_output}, but got {result}"

    def test_malformed_input(self):
        input_list = ["User-agent *"]
        with pytest.raises(ValueError):
            _can_webscrape.robot_list_to_dict(input_list)


class TestDictionaryToLowercase:
    def test_dict_keys_to_lowercase(self):
        input_dict = {
        "Disallow": ["/admin", "/login"],
        "User-agent": ["*"]
        }
        expected_output_dict = {
        "disallow": ["/admin", "/login"],
        "user-agent": ["*"]
        }
        result = _can_webscrape.dict_keys_to_lowercase(input_dict)
        assert result == expected_output_dict, f"Expected {expected_output_dict}, but got {result}"


class TestCanWebscrape:
    @pytest.mark.parametrize("robots_txt_dict, expected", [
        ({"User-agent": "*", "Disallow": "/", "Allow": "", "Sitemap" : "", "Crawl-delay" : "", "Host" : "", "Clean-param" : "", "Request-rate" : "", "Visit-Time" : "", "No-index" : "", "Wildcard Entires" : ""}, {"allowed": False, "disallowed_directories": ["/"]}),
        ({"user-agent": "Googlebot", "disallow": ["/"]}, {"allowed": True, "disallowed_directories": []}), # As you've hardcoded User-agent to "*", this should return True
        ({"user-agent": "*", "disallow": ["/admin", "/"]}, {"allowed": False, "disallowed_directories": ["/"]}),
        ({"user-agent": "*", "disallow": ["/admin", "/dashboard"]}, {"allowed": True, "disallowed_directories": ["/admin", "/dashboard"]}),
    ])
    def test_can_webscrape(self, robots_txt_dict, expected):
        input_dict = _can_webscrape.dict_keys_to_lowercase(robots_txt_dict)
        result = _can_webscrape.can_webscrape(input_dict)
        assert  result == expected, f"Expected {expected}, but got {result}"


class TestWebscrapeBehavioral:
    @pytest.mark.parametrize("robots_txt_content, expected_decision", [
        ("User-agent: *\nDisallow: /", {"allowed": False, "disallowed_directories": ["/"]}),
        ("User-agent: *\nDisallow: /admin", {"allowed": True, "disallowed_directories": ["/admin"]}),
        ("User-agent: Googlebot\nDisallow: /", {"allowed": True, "disallowed_directories": []}),
        ("""
        User-agent: *
        Disallow: /admin
        """, 
        {"allowed": True, "disallowed_directories": ["/admin"]}),
        ("""
        User-agent: Googlebot
        Disallow: /
        """, 
        {"allowed": True, "disallowed_directories": []}),
        ("""
        User-agent: sitebot
        Disallow: /
        
        User-agent: MJ12bot
        Disallow: /
        
        User-agent: *
        Disallow: /favourites
        Disallow: /recommendations
        Disallow: /refer-a-friend
        Disallow: /account
        Disallow: /account/
        Disallow: /members/sign-up-details
        Disallow: /members/verify
        Disallow: /members/reset
        Disallow: /watchlist
        
        sitemap: https://smarkets.com/sitemap.xml
        """,
        {"allowed": True, "disallowed_directories": ["/favourites", "/recommendations", "/refer-a-friend", "/account", "/account/", "/members/sign-up-details", "/members/verify", "/members/reset", "/watchlist"]})
    ])
    @patch('requests.get')
    def test_webscrape_behavior(self, mock_get, robots_txt_content, expected_decision):
        # Given a URL that has a robots.txt
        url = "http://example.com/robots.txt"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = robots_txt_content
        mock_get.return_value = mock_response
        
        scrape_decision = _can_webscrape.can_webscrape_main(url)
        assert scrape_decision == expected_decision, f"Expected {expected_decision}, but got {scrape_decision}"

