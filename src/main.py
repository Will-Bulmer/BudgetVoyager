import _can_webscrape

response = _can_webscrape.fetch_robots_txt("https://smarkets.com/robots.txt")
print(response)

