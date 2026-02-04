# Getting Started Guide

This guide will walk you through the process of setting up and using the JW.org Study Bible scraper.

## Step 1: Environment Setup

### Install Python
Ensure you have Python 3.8 or higher installed:
```bash
python --version
```

If you need to install Python, visit [python.org](https://www.python.org/downloads/).

### Create Virtual Environment
It's recommended to use a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- selenium (browser automation)
- beautifulsoup4 (HTML parsing)
- lxml (fast parsing)
- requests (HTTP requests)
- pandas (data handling)

### Install ChromeDriver

Selenium requires ChromeDriver to control Chrome browser:

**Option 1: Automatic (recommended)**
```bash
pip install webdriver-manager
```

Then update the scraper to use:
```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
```

**Option 2: Manual**
1. Check your Chrome version: chrome://version
2. Download matching ChromeDriver from [chromedriver.chromium.org](https://chromedriver.chromium.org/)
3. Add to PATH or place in project directory

## Step 2: Understand the Webpage

Before scraping, understand the target webpage structure:

### Analyze the Structure
```bash
python examples/analyze_structure.py
```

This script will:
1. Open the JW.org Study Bible books page
2. Inspect HTML elements
3. Save page source for manual review
4. Display analysis results

### Manual Inspection

1. **Open the webpage** in your browser:
   https://www.jw.org/en/library/bible/study-bible/books/

2. **Open Developer Tools** (F12 or right-click → Inspect)

3. **Inspect key elements**:
   - Book links in the navigation
   - Chapter selectors
   - Verse containers
   - Study note panels

4. **Monitor Network tab**:
   - Load a chapter
   - Watch for AJAX/XHR requests
   - Note endpoint URLs and response formats

### Review Documentation

Read the detailed structure analysis:
```bash
cat docs/WEBPAGE_STRUCTURE.md
```

## Step 3: Test Basic Scraping

### Test 1: Get Books List

Create a test file `test_books.py`:

```python
from src.scrapers.bible_scraper import BibleScraper

def test_books_list():
    scraper = BibleScraper(headless=False)  # Set False to see browser
    
    try:
        books = scraper.get_books_list()
        print(f"\nFound {len(books)} books\n")
        
        for book in books[:5]:  # Show first 5
            print(f"- {book['name']}")
            print(f"  URL: {book['url']}")
            print()
            
    finally:
        scraper.close_driver()

if __name__ == "__main__":
    test_books_list()
```

Run it:
```bash
python test_books.py
```

### Test 2: Get Chapter Content

Create `test_chapter.py`:

```python
from src.scrapers.bible_scraper import BibleScraper
from src.utils.storage import DataStorage

def test_chapter():
    scraper = BibleScraper(headless=False)
    storage = DataStorage()
    
    try:
        # Get Genesis chapter 1
        chapter_data = scraper.get_chapter_content('/genesis', 1)
        
        print(f"\nChapter data structure:")
        print(f"- Chapter: {chapter_data['chapter']}")
        print(f"- Verses: {len(chapter_data['verses'])}")
        print(f"- Study notes: {len(chapter_data['study_notes'])}")
        
        # Save data
        filepath = storage.save_chapter_data('Genesis', 1, chapter_data)
        print(f"\nSaved to: {filepath}")
        
    finally:
        scraper.close_driver()

if __name__ == "__main__":
    test_chapter()
```

Run it:
```bash
python test_chapter.py
```

## Step 4: Update Selectors

The scraper includes placeholder CSS selectors that need to be updated based on the actual webpage:

### Identify Correct Selectors

1. **Open the saved HTML** from step 2:
   ```bash
   # Open in browser or text editor
   open examples/page_source_sample.html
   ```

2. **Find verse containers**:
   - Look for elements containing verse text
   - Note the class names or IDs
   - Example: `<p class="sb">` or `<div class="verse">`

3. **Find study notes**:
   - Look for study note panels
   - Note how they're structured
   - Example: `<div class="studyNote">`

### Update the Scraper

Edit `src/scrapers/bible_scraper.py`:

```python
# Update these selectors based on your findings
BOOK_LINK_SELECTOR = 'a.bookLink'  # Update this
VERSE_SELECTOR = 'p.verse'         # Update this
STUDY_NOTE_SELECTOR = 'div.studyNote'  # Update this
```

### Update the Parser

Edit `src/parsers/html_parser.py`:

```python
# Update selectors in extract methods
verse_elements = self.soup.find_all('p', class_='YOUR_CLASS_HERE')
```

## Step 5: Implement Data Collection

### Create a Collection Script

Create `collect_data.py`:

```python
from src.scrapers.bible_scraper import BibleScraper
from src.parsers.html_parser import StudyBibleParser
from src.utils.storage import DataStorage
import time

def collect_book(book_name, book_url, chapter_count):
    """Collect all chapters for a book."""
    scraper = BibleScraper(headless=True)
    storage = DataStorage()
    parser = StudyBibleParser("")
    
    try:
        book_data = {
            'name': book_name,
            'chapters': []
        }
        
        for chapter_num in range(1, chapter_count + 1):
            print(f"Collecting {book_name} chapter {chapter_num}...")
            
            # Get chapter content
            chapter_data = scraper.get_chapter_content(book_url, chapter_num)
            book_data['chapters'].append(chapter_data)
            
            # Be respectful: wait between requests
            time.sleep(3)
            
        # Save complete book
        storage.save_book_data(book_name, book_data)
        print(f"✓ Completed {book_name}")
        
    finally:
        scraper.close_driver()

# Example: Collect Genesis (50 chapters)
collect_book('Genesis', '/genesis', 50)
```

## Step 6: Monitor and Debug

### Enable Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
```

### Handle Errors

```python
from selenium.common.exceptions import TimeoutException, NoSuchElementException

try:
    element = driver.find_element(By.CLASS_NAME, 'verse')
except TimeoutException:
    print("Element took too long to load")
except NoSuchElementException:
    print("Element not found on page")
```

### Check Data Quality

```python
def validate_chapter_data(data):
    """Validate scraped data."""
    assert data['chapter'] > 0, "Invalid chapter number"
    assert len(data['verses']) > 0, "No verses found"
    print(f"✓ Validation passed: {len(data['verses'])} verses")

# Use it
chapter_data = scraper.get_chapter_content('/genesis', 1)
validate_chapter_data(chapter_data)
```

## Step 7: Scale Up

### Scrape Multiple Books

```python
books_to_scrape = [
    {'name': 'Genesis', 'url': '/genesis', 'chapters': 50},
    {'name': 'Exodus', 'url': '/exodus', 'chapters': 40},
    # ... more books
]

for book in books_to_scrape:
    collect_book(book['name'], book['url'], book['chapters'])
    time.sleep(10)  # Pause between books
```

### Resume from Interruption

```python
from src.utils.storage import DataStorage

def get_completed_books():
    """Get list of already scraped books."""
    storage = DataStorage()
    return storage.get_all_saved_books()

# Skip already completed
completed = get_completed_books()
remaining = [b for b in books_to_scrape if f"{b['name']}.json" not in completed]
```

## Best Practices

### 1. Rate Limiting
```python
import time

# Wait between requests
time.sleep(3)  # 3 seconds

# Random delays to appear more natural
import random
time.sleep(random.uniform(2, 5))
```

### 2. Error Recovery
```python
max_retries = 3
for attempt in range(max_retries):
    try:
        data = scraper.get_chapter_content(url, chapter)
        break
    except Exception as e:
        if attempt < max_retries - 1:
            time.sleep(5)
            continue
        else:
            raise
```

### 3. Data Validation
```python
def validate_verse(verse):
    """Check if verse data is complete."""
    required_fields = ['number', 'text']
    return all(field in verse for field in required_fields)
```

### 4. Progress Tracking
```python
total_chapters = 50
for i, chapter in enumerate(range(1, total_chapters + 1), 1):
    print(f"Progress: {i}/{total_chapters} ({i/total_chapters*100:.1f}%)")
    # scrape chapter
```

## Troubleshooting

### ChromeDriver Issues
```
WebDriverException: unknown error: cannot find Chrome binary
```
**Solution**: Install Chrome browser or specify Chrome location:
```python
options.binary_location = "/path/to/chrome"
```

### Timeout Errors
```
TimeoutException: Message: timeout
```
**Solution**: Increase wait time:
```python
scraper = BibleScraper(wait_time=30)  # 30 seconds
```

### Element Not Found
```
NoSuchElementException: Unable to locate element
```
**Solution**: 
1. Verify selector is correct
2. Check if element loads dynamically
3. Add explicit wait
4. Inspect page source

### Website Blocking
```
HTTP 403 Forbidden
```
**Solution**:
1. Add user agent
2. Increase delays
3. Consider using proxies
4. Contact website for API access

## Next Steps

1. **Refine selectors** based on actual HTML structure
2. **Implement complete parser** for all content types
3. **Add database storage** for relational data
4. **Create export tools** (PDF, EPUB, etc.)
5. **Build analysis tools** for the scraped data

## Additional Resources

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Python Requests](https://requests.readthedocs.io/)
- Web Scraping Best Practices

## Support

If you encounter issues:
1. Check the logs in `scraper.log`
2. Review saved HTML files
3. Verify network connectivity
4. Check for website changes
5. Open an issue on GitHub
