#!/usr/bin/env python3

import _can_webscrape

#response = _can_webscrape.fetch_robots_txt("https://smarkets.com/robots.txt")
#print(response)

decision_list = _can_webscrape.can_webscrape_main("https://www.flixbus.com/robots.txt")
print(decision_list)

