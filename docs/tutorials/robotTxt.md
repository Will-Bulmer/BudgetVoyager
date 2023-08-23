# Guide to `robots.txt`

`robots.txt` is a standard used by websites to direct web crawling and scraping bots about which pages or files the bot can or can't request from a site.

## Basic Structure

Each entry in `robots.txt` is a group of directives (i.e., lines specifying a rule), and it looks something like:

```plaintext
User-agent: [name of bot]
Directive: [path or pattern]
```

## Directives

### 1. `User-agent`
- **Purpose**: Specifies which bot the rule applies to.
- **Options**:
  - `*`: applies to all bots
  - `[name of bot]`: applies to a specific bot (e.g., `Googlebot`)
- **Examples**:
  - `User-agent: *`: applies to all bots
  - `User-agent: Googlebot`: applies only to Google’s web crawling bot

### 2. `Disallow`
- **Purpose**: Tells the bot not to access specific pages or directories.
- **Options**:
  - `/path/`: Disallows crawling of a specific directory.
  - `/filename.html`: Disallows crawling of a specific file.
- **Examples**:
  - `Disallow: /private/`: bots should not crawl anything in the `private` directory.
  - `Disallow: /secrets.html`: bots should not crawl the `secrets.html` page.

### 3. `Allow`
- **Purpose**: Explicitly allows access to specific pages or directories, useful especially if you're using a `Disallow` directive at a higher level.
- **Options**: Same as `Disallow`.
- **Examples**:
  - Given `Disallow: /private/`
  - `Allow: /private/public_page.html`: this would let bots crawl `public_page.html` inside the `private` directory.

### 4. `Crawl-delay`
- **Purpose**: Sets a delay between successive requests to the server. Not supported by all bots.
- **Options**: Number of seconds to wait.
- **Example**: 
  - `Crawl-delay: 10`: bots should wait 10 seconds between requests.

### 5. `Sitemap`
- **Purpose**: Points to the sitemap for the website.
- **Options**: URL of the sitemap.
- **Example**: 
  - `Sitemap: https://www.example.com/sitemap.xml`

## Wildcards

- `*`: Represents any sequence of characters.
  - `Disallow: /*.html`: Disallows all URLs ending in `.html`.
- `$`: Specifies the end of a URL.
  - `Disallow: /*.php$`: Disallows all URLs ending in `.php`.

## Example `robots.txt` File

```plaintext
User-agent: *
Disallow: /private/
Allow: /private/public_page.html
Crawl-delay: 10
Sitemap: https://www.example.com/sitemap.xml
```

## Important Notes

1. Paths in `Disallow` and `Allow` are case-sensitive on some servers.
2. The `robots.txt` file should be located at the root of the website, e.g., `https://www.example.com/robots.txt`.
3. If a `User-agent` has both `Allow` and `Disallow` directives, the most specific rule based on path length will take precedence.
4. The `robots.txt` is a standard, but not enforceable. Respectful bots will follow it, but it doesn't guarantee that all bots will.

