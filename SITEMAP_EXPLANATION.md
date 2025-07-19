# WebChecker: Sitemap Functionality & Text Extraction Improvements

## 🔧 **Text Extraction Improvements**

### **Problem Solved**
The original text extraction was grabbing too much content across line boundaries and including unwanted punctuation.

### **Before (Problematic)**
```
Text: "Contact us at john@example.com.\nNext line content here."
Result: "john@example.com.\nNext line content here"  ❌ Too much text!
```

### **After (Fixed)**
```
Text: "Contact us at john@example.com.\nNext line content here."
Result: "john@example.com"  ✅ Perfect!
```

### **Key Improvements**

1. **Line Break Respect**: Stops at `\n`, `\r`, `\t` characters
2. **Punctuation Boundaries**: Stops at `.,;:!?()[]{}<>"'`
3. **HTML Character Handling**: Stops at HTML-like characters
4. **Trailing Punctuation Removal**: Automatically removes `.,;:!?` from results
5. **Control Character Detection**: Stops at any character with ASCII code < 32

### **Boundary Detection Logic**
```python
# Stop at these characters:
- Whitespace: space, tab, newline, carriage return
- Punctuation: .,;:!?()[]{}<>"'
- Control characters: ASCII < 32
- HTML-like characters: <, >, etc.
```

## 🗺️ **Sitemap Functionality Explained**

### **What is `follow_sitemap`?**

The `follow_sitemap` parameter controls whether WebChecker should discover and scrape URLs from the website's sitemap before starting the regular crawling process.

### **How It Works**

#### **When `follow_sitemap=True` (Default in Web Interface):**

1. **Sitemap Discovery**: WebChecker looks for sitemaps at:
   - `/sitemap.xml`
   - `/sitemap_index.xml`
   - `/robots.txt` (for sitemap references)

2. **URL Extraction**: Parses the sitemap to find all available pages

3. **Priority Crawling**: Adds all sitemap URLs to the crawl queue with depth 0

4. **Comprehensive Coverage**: Ensures you don't miss important pages

#### **When `follow_sitemap=False`:**

1. **Direct Crawling**: Starts crawling from the provided URL only
2. **Link Discovery**: Finds new pages by following links on each page
3. **Depth-Based**: Relies on the `max_depth` parameter to control exploration

### **Example Scenarios**

#### **Scenario 1: `follow_sitemap=True`**
```
Starting URL: https://example.com/
Sitemap found: https://example.com/sitemap.xml
Sitemap contains: 50 URLs
Result: All 50 URLs are queued for scraping (if within max_pages limit)
```

#### **Scenario 2: `follow_sitemap=False`**
```
Starting URL: https://example.com/
No sitemap lookup
Result: Only pages reachable by following links from the starting page
```

### **When to Use Each Option**

#### **Use `follow_sitemap=True` When:**
- ✅ You want comprehensive coverage of the entire website
- ✅ The website has a well-maintained sitemap
- ✅ You want to find patterns across all pages, not just linked pages
- ✅ You're doing a thorough audit or analysis

#### **Use `follow_sitemap=False` When:**
- ✅ You only want to scrape pages reachable from the starting URL
- ✅ The website doesn't have a sitemap
- ✅ You want faster, more focused scraping
- ✅ You're only interested in content linked from the main page

### **Performance Impact**

#### **`follow_sitemap=True`:**
- **Pros**: More comprehensive, finds hidden pages
- **Cons**: Slower startup (must fetch and parse sitemap), may hit rate limits

#### **`follow_sitemap=False`:**
- **Pros**: Faster startup, more focused results
- **Cons**: May miss important pages not linked from the starting URL

### **Web Interface Default**

The web interface defaults to `follow_sitemap=True` because:
1. **Better User Experience**: Users typically want comprehensive results
2. **More Complete Coverage**: Finds patterns across the entire site
3. **Professional Use Case**: Most users want thorough analysis

### **Command Line Control**

```bash
# Use sitemap (default)
webchecker https://example.com --pattern "@"

# Skip sitemap for faster, focused scraping
webchecker https://example.com --pattern "@" --no-sitemap
```

## 🎯 **Real-World Example**

### **Finding Email Addresses on a Company Website**

#### **With Sitemap (`follow_sitemap=True`):**
```
Starting URL: https://company.com/
Sitemap URLs: 25 pages (about, team, contact, services, etc.)
Results: Emails found across all 25 pages
Time: 2-3 minutes
Coverage: 100% of website
```

#### **Without Sitemap (`follow_sitemap=False`):**
```
Starting URL: https://company.com/
Linked pages: 8 pages (only those linked from homepage)
Results: Emails found on 8 pages only
Time: 30 seconds
Coverage: ~30% of website
```

## 🔧 **Technical Implementation**

### **Sitemap Discovery Process**
```python
def _discover_sitemap_urls(self, base_url: str) -> List[str]:
    sitemap_locations = [
        urljoin(base_url, '/sitemap.xml'),
        urljoin(base_url, '/sitemap_index.xml'),
        urljoin(base_url, '/robots.txt')
    ]
    
    for location in sitemap_locations:
        try:
            response = self.session.get(location, timeout=self.timeout)
            if location.endswith('robots.txt'):
                urls.extend(self._parse_robots_txt(response.text, base_url))
            else:
                urls.extend(self._parse_sitemap_xml(response.text))
        except requests.RequestException:
            continue
```

### **Text Extraction Boundary Detection**
```python
# Stop at these boundaries:
if (char.isspace() or char in '.,;:!?()[]{}<>"\'' or 
    char in '\n\r\t' or ord(char) < 32):
    break
```

This ensures clean, precise text extraction that respects natural text boundaries and doesn't include unwanted content from adjacent lines or paragraphs. 