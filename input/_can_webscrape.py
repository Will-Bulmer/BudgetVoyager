import requests
import re

def fetch_robots_txt(url: str) -> str:
    if not url.endswith("robots.txt"):
        raise Exception(f"Invalid URL '{url}'. The URL should end with 'robots.txt'")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch robots.txt from {url}. RESPONSE CODE: {response.status_code}")
    return response.text.strip()

def separate_robot_txt_by_groups(robots_txt: str) -> list:
    pattern = re.compile(
        r"((user-agent:|allow:|disallow:|crawl-delay:|sitemap:|host:)\s*(?:(?!user-agent:|allow:|disallow:|crawl-delay:|sitemap:|host:).)*)",
        re.IGNORECASE
    )
    matches = pattern.findall(robots_txt)
    lines = [match[0].strip() for match in matches]
    return lines

def filter_user_agent(input_list):
    # Regex patterns
    user_agent_star_pattern = re.compile(r"User-agent: \*", re.IGNORECASE)
    user_agent_not_star_pattern = re.compile(r"User-agent: (?!.*\*)[^\n]+", re.IGNORECASE)
    rules_pattern = re.compile(r"(Disallow: [^\s]+|Allow: [^\s]+|Crawl-delay: \d+)", re.IGNORECASE)
    global_pattern = re.compile(r"(Sitemap: [^\s]+|Host: [^\s]+)", re.IGNORECASE)

    output = []
    should_apply_rules = False
    user_agent_star_added = False

    for line in input_list:
        line = line.strip()

        # Match "User-agent: *"
        if user_agent_star_pattern.match(line):
            should_apply_rules = True
            if not user_agent_star_added:
                output.append(line)
                user_agent_star_added = True
            continue

        # Match "User-agent" that isn't "*"
        if user_agent_not_star_pattern.match(line):
            should_apply_rules = False
            user_agent_star_added = False
            continue

        # Match rules when "User-agent: *" is active
        if should_apply_rules and rules_pattern.match(line):
            output.append(line)
            continue

        # Match global directives
        if global_pattern.match(line):
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
    
    if user_agent and "*" in user_agent:  # changed this line to check for presence of "*" in user_agent
        if "/" in disallow:
            print("You cannot scrape this website.")
            return {"allowed": False, "disallowed_directories": ["/"]}
        elif disallow:  # Check if disallow has any content
            print("You can scrape this website.")
            print("However, avoid the following directories:", disallow)
            return {"allowed": True, "disallowed_directories": disallow}
        
    # If no disallow key is found or user-agent isn't "*", assume scraping is allowed
    print("You can scrape this website.")
    return {"allowed": True, "disallowed_directories": []}


def can_webscrape_main(url: str) -> dict:
    fetched_content = fetch_robots_txt(url)
    robots_list = separate_robot_txt_by_groups(fetched_content)
    robots_filtered_list = filter_user_agent(robots_list)
    robots_dict = robot_list_to_dict(robots_filtered_list)
    robots_dict_lower = dict_keys_to_lowercase(robots_dict)
    scrape_decision = can_webscrape(robots_dict_lower)
    
    return scrape_decision



