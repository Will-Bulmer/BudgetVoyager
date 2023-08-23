import requests
import re

def fetch_robots_txt(url: str) -> str:
    if not url.endswith("robots.txt"):
        raise Exception(f"Invalid URL '{url}'. The URL should end with 'robots.txt'")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch robots.txt from {url}")
    return response.text.strip()


def convert_robot_txt_to_list(robots_txt: str) -> list:
    lines = robots_txt.split('\n') # Split a string into a list
    # Regular expression pattern to recognize robot rules
    pattern = re.compile(r"(User-agent: \*|Disallow: [^\s]+|Allow: [^\s]+|Crawl-delay: \d+|Sitemap: [^\s]+|Host: [^\s]+)")
    return [match for line in lines for match in pattern.findall(line)] # Regex findall method

def filter_by_user_agent(lines):
    
    # Regex patterns
    user_agent_pattern = re.compile(r"User-agent: \*", re.IGNORECASE)
    rules_pattern = re.compile(r"(Disallow: [^\s]+|Allow: [^\s]+|Crawl-delay: \d+)", re.IGNORECASE)
    global_pattern = re.compile(r"(Sitemap: [^\s]+|Host: [^\s]+)", re.IGNORECASE)

    output = []
    apply_rules = False
    for line in lines:

        if user_agent_pattern.match(line):
            apply_rules = True
            output.append(line)  # Add the User-agent line to the output
            continue
        
        if apply_rules and (rules_pattern.match(line) or global_pattern.match(line)):
            output.append(line)
    return output


def robot_list_to_dict(input_list):
    output_dict = {}
    
    for item in input_list:
        key, value = item.split(": ")
        if key in output_dict:
            output_dict[key].append(value)
        else:
            output_dict[key] = [value]
    
    return output_dict

def dict_keys_to_lowercase(input_dict):
    return {k.lower(): v for k, v in input_dict.items()}
    
def can_webscrape(robots_txt_dict):
    user_agent = robots_txt_dict.get("user-agent")
    disallow = robots_txt_dict.get("disallow", [])
    
    if user_agent == "*":
        if "/" in disallow:
            print("You cannot scrape this website.")
            return {"allowed": False, "disallowed_directories": ["/"]}
        
        print("You can scrape this website.")
        print("However, avoid the following directories:", disallow)
        return {"allowed": True, "disallowed_directories": disallow}
    
    # If no disallow key is found or user-agent isn't "*", assume scraping is allowed
    print("You can scrape this website.")
    return {"allowed": True, "disallowed_directories": []}





