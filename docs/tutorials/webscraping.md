## Tips for the Webscraping Needed for this Project

### Things to Look For:
1. **Static Data**: Sometimes, the data you need is rendered directly in the HTML and can be scraped without making additional requests.

2. **Dynamic Data Loading**:

    - Navigate to the `Network tab` in the developer tools.
    - Reload the page (`F5` or `Ctrl + R`).
    - Here, you'll see all network requests made by the page. Look for any AJAX or XHR requests, especially those returning JSON or other structured data.
    - Filter by "XHR" to see only the dynamically loaded content requests.
    - Investigate these requests to see if they contain the route data you're looking for.

3. **Scripts & Data Initialization**:

Some websites embed data within JavaScript scripts, typically as initialization data for web apps. Look for `<script>` tags in the page source and see if they contain large JSON objects or arrays, which might be the route data.

4. **Pagination & Infinite Scrolling**:

If the page has pagination or loads more data as you scroll, take note of how this happens. There may be AJAX requests fetching additional data as you interact with the page.

### Strategies to Avoid Flags:
1. **Rate Limiting**: Introduce delays between requests. If you're using Python's requests library, you can use time.sleep() to introduce delays.

2. **User Agent Rotation**: Change the User Agent for each request to mimic different browsers/devices.

3. **Proxy Rotation**: Use a list of proxies and rotate through them for different requests. This makes it look like the requests are coming from different IP addresses.

4. **Headers & Cookies**: Ensure your scraper sends all necessary headers and cookies, mimicking a real browser's behavior.

5. **Respect robots.txt**: Always check the website's `robots.txt` to see which paths are allowed to be scraped.

Remember that scraping can be a gray area both ethically and legally. Always ensure that you're respectful of the website's terms of service, and if in doubt, consider reaching out to the website's administrators or legal team.

## Common XHR Requests
The primary use of XMLHttpRequest is to retrieve data from a server after a web page has loaded, allowing web pages to be updated asynchronously by exchanging data with a web server behind the scenes.

### Cities
https://global.api.flixbus.com/search/service/cities/details?locale=en_GB&from_city_id=5415b966-f8b8-4b27-8620-1641c1a43e45

[cities](https://global.api.flixbus.com/search/autocomplete/cities?q=Manchester&lang=en&country=gb&flixbus_cities_only=false&stations=false)

### Money

https://global.api.flixbus.com/cms/cities/e8aae13c-1801-4553-b103-e10e8500d4e8/reachable?language=en-gl&country=GB&limit=5

https://global.api.flixbus.com/search/service/v4/search?from_city_id=e8aae13c-1801-4553-b103-e10e8500d4e8&to_city_id=5415b966-f8b8-4b27-8620-1641c1a43e45&departure_date=24.08.2023&products=%7B%22adult%22%3A1%7D&currency=GBP&locale=en_GB&search_by=cities&include_after_midnight_rides=1

**Referral Source**: Some APIs or web services might allow requests from browsers due to the referral source (e.g., from the official website), while blocking other types of requests. This is especially true for services that are integrated into web applications.

### Attempt to Find Endpoints
