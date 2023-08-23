## Design Plan

The aim of this software is to pool together an incredibly large sample of bus routes, train routes and plane routes, and create an algorithm that can find me a journey based on certain parameters: upperBoundMoney and upperBoundTime. I would like for it to display the top 5 journeys.

*Here is my plan*:
1. Webscrape/ API flixbus routes 14:00 finish

- Create test that can verify robots.txt file
- Create function that can generate the robots.txt file

2. Webscrape/ API megabus routes 15:00 finish
3. Webscrape/ API Trainline routes 16:00 finish

-- Break --

Using this data, create matrices that contains nodes for locations with prices and length attached to them. I will then delve into decision theory in order to create an algorithm which can give me the desired output.