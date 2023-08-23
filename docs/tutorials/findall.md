## Guide to `re.findall()` in Python

The `re.findall()` method is a powerful tool provided by Python's `re` (regular expressions) module. It's designed to find all non-overlapping matches of a pattern in a string and return them as a list.

### **Syntax:**

```python
re.findall(pattern, string, flags=0)
```
- `pattern`: The regular expression pattern to search for.
- `string`: The string in which to search for the pattern.
- `flags` (optional): Modifiers that change how the search is performed, e.g., re.IGNORECASE for case-insensitive matching.

### **Basic Usage**
```python
import re

string = "The rain in Spain falls mainly on the plain."
pattern = r'\b\w+ain\b'
matches = re.findall(pattern, string)
print(matches)  # ['rain', 'Spain', 'plain']
```
### **Using Capturing Groups**
If your pattern includes capturing groups (parts of the regex pattern enclosed in parentheses), the returned list will contain tuples, with each tuple holding the matched values for the groups.
```python
pattern = r"(\b\w+ain\b) (\bin\b)"
matches = re.findall(pattern, string)
print(matches)  # [('rain', 'in'), ('Spain', 'in')]
```

### **Common Flags**
- `re.IGNORECASE`: Performs case-insensitive matching.
- `re.MULTILINE`: Makes ^ and $ match the start/end of each line.

### **Examples**
1. **Case-Insensitive Matching**
```python
pattern = r"the"
matches = re.findall(pattern, string, re.IGNORECASE)
print(matches)  # ['The', 'the']
```

2. **Extracting Email Addresses**
```python
text = "Reach out at contact@example.com and hello@world.net."
pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
emails = re.findall(pattern, text)
print(emails)  # ['contact@example.com', 'hello@world.net']
```

### **Notes**
- Non-capturing groups `(?:...)`s do not return captured values in the result. They're used when you want to group parts of your pattern but don't need to extract the matched content.