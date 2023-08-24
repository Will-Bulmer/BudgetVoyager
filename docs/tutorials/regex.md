## Guide to Regex Used in This Software

### 1. User-agent Group

```regex
(?P<useragent>User-agent:\s?.+?)(?=Disallow:|Allow:|sitemap:|Crawl-delay:|Host:|$)
```
- `(?P<useragent> ... )`: This is a named capture group. The content inside the parentheses will be captured and associated with the name `useragent`.
- `User-agent:\s?`: This matches the string "User-agent:", possibly followed by a space (`\s?` means "zero or one space").
- `.+?`: This matches one or more of any character (.) in a non-greedy manner (`?` after `+` makes it non-greedy). This means it will capture as few characters as necessary until the next pattern matches.
- `(?= ... )`: This is a positive lookahead. It checks if the pattern inside the parentheses exists ahead in the string but doesn't consume any characters. It's used to stop the non-greedy match when one of the following patterns is found.

### 2. Disallow Group
```regex 
(?P<disallow>Disallow:\s?.+?)(?=User-agent:|Allow:|sitemap:|Crawl-delay:|Host:|$)
```
- Structured similarly to the `User-agent` group, this captures content following "Disallow:".

### 3. Allow Group
```regex
(?P<allow>Allow:\s?.+?)(?=User-agent:|Disallow:|sitemap:|Crawl-delay:|Host:|$)
```
- This captures content following "Allow:".

etc..

### 4. Overall Structure
1. Match the field name.
2. Capture everything non-greedily until one of the other fields or the end of the string is encountered.

The advantage of the non-greedy `.+?` combined with the positive lookahead is that it ensures each group captures its content without encroaching on the next field's territory.

In simpler terms, this regex pattern is designed to separate the different fields in a robots.txt-like string, even if the string doesn't have standard line breaks.

### 5. Example
```regex
(user-agent:|allow:|disallow:|crawl-delay:|sitemap:|host:)(?:\s|$)[^uadchs]*(?=(?:user-agent:|allow:|disallow:|crawl-delay:|sitemap:|host:|$))
```
1. **Capturing Group for Directives**
```regex
(user-agent:|allow:|disallow:|crawl-delay:|sitemap:|host:)
```
    - This is a capturing group `( ... )` that matches any one of the listed directives. The `|` acts as an OR operator, so the regex will try to match any one of the mentioned directives.

2. **Non-capturing Group for Whitespace or End**
```regex
(?:\s|$)
```
- `(?: ... )` is a non-capturing group. It groups elements of the regex together without capturing the matched content.
- `\s` matches any whitespace character (like spaces, tabs, and line breaks).
- `|` acts as an OR operator.
- `$` matches the end of a line or string.
- So, `(?:\s|$)` matches either a whitespace or the end of a string. This is useful for cases where a directive might be at the end of a robots.txt without any following whitespace or other content.

3. **Match everything until the next directive**
```regex
[^uadchs]*
```
- `[^...]` is a negated character set. It matches any character NOT in the set.
- The characters `uadchs` are the starting characters of our directives (`user-agent:`, `allow:`, `disallow:`, `crawl-delay:`, `sitemap:`, `host:`). By excluding these, we're saying "match anything that doesn't look like the beginning of a new directive".
- `*` is a quantifier that matches the preceding element (the negated character set in this case) zero or more times.
- So, `[^uadchs]*` captures all content until it sees something that looks like the start of another directive.

4. **Positive Lookahead for the Next Directive or End**
```regex
(?=(?:user-agent:|allow:|disallow:|crawl-delay:|sitemap:|host:|$))
```
- `(?= ... )` is a positive lookahead. It checks for a pattern without consuming any characters. It's a way of saying "look ahead to see if there's X, but don't move the cursor forward".
- The inner `(?: ... )` is a non-capturing group.
- Inside the non-capturing group, we again list all the directives OR the end of the string `$`.
- The lookahead ensures that our previous match stops when it sees another directive or reaches the end of the string.