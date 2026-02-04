"""
Complete Integration Example: Bible Scraping Workflow

This example demonstrates a complete workflow for scraping Bible content
using Playwright MCP tools, parsing the data, and storing it.

This is a documentation example showing how all components work together.
"""

from typing import Dict, List
import json
import time


def example_complete_workflow():
    """
    Complete workflow example showing all steps.
    
    This is a pseudo-code example demonstrating the pattern.
    In actual usage, you would use the MCP Playwright tools directly.
    """
    
    print("=" * 80)
    print("COMPLETE BIBLE SCRAPING WORKFLOW")
    print("=" * 80)
    print()
    
    # Step 1: Initialize components
    print("Step 1: Initialize Components")
    print("-" * 80)
    print("""
from src.scrapers.playwright_scraper import PlaywrightBibleScraper
from src.parsers.html_parser import StudyBibleParser
from src.utils.storage import DataStorage

scraper = PlaywrightBibleScraper(headless=True)
storage = DataStorage()
    """)
    
    # Step 2: Navigate to books list
    print("\nStep 2: Get Books List")
    print("-" * 80)
    print("""
# Using Playwright MCP:
playwright-browser_navigate(
    url="https://www.jw.org/en/library/bible/study-bible/books/"
)
playwright-browser_wait_for(time=2)
snapshot = playwright-browser_snapshot()

# Parse snapshot to extract books
books = parse_books_from_snapshot(snapshot)
# Result: [{"name": "Genesis", "url": "/genesis", ...}, ...]
    """)
    
    # Step 3: Scrape individual book
    print("\nStep 3: Scrape Individual Book (Genesis)")
    print("-" * 80)
    print("""
book = books[0]  # Genesis
book_data = {
    "name": book["name"],
    "chapters": []
}

# Iterate through chapters (Genesis has 50)
for chapter_num in range(1, 51):
    print(f"Scraping Genesis chapter {chapter_num}...")
    
    # Navigate to chapter
    chapter_url = f"https://www.jw.org/.../genesis/{chapter_num}/"
    playwright-browser_navigate(url=chapter_url)
    playwright-browser_wait_for(time=2)
    
    # Get chapter content
    chapter_snapshot = playwright-browser_snapshot()
    
    # Parse chapter data
    chapter_data = parse_chapter_from_snapshot(chapter_snapshot)
    book_data["chapters"].append(chapter_data)
    
    # Rate limiting: wait between chapters
    time.sleep(3)
    """)
    
    # Step 4: Extract verses
    print("\nStep 4: Extract Verses")
    print("-" * 80)
    print("""
def parse_chapter_from_snapshot(snapshot):
    verses = []
    
    # Parse snapshot for verse elements
    # Look for patterns like:
    #   text "1 In the beginning..."
    #   text "2 Now the earth..."
    
    for line in snapshot.split('\\n'):
        if is_verse_line(line):
            verse_num = extract_verse_number(line)
            verse_text = extract_verse_text(line)
            verses.append({
                "number": verse_num,
                "text": verse_text
            })
    
    return {
        "chapter": chapter_num,
        "verses": verses
    }
    """)
    
    # Step 5: Extract study notes
    print("\nStep 5: Extract Study Notes")
    print("-" * 80)
    print("""
# Click on study note marker to reveal note
playwright-browser_click(
    element="Study note for verse 1",
    ref="<ref from snapshot>"
)
playwright-browser_wait_for(time=1)

# Get updated snapshot with note visible
note_snapshot = playwright-browser_snapshot()

# Parse study note
study_note = {
    "verse_reference": "1:1",
    "content": extract_note_content(note_snapshot)
}
    """)
    
    # Step 6: Save data
    print("\nStep 6: Save Data")
    print("-" * 80)
    print("""
# Save book data to JSON
storage.save_book_data("Genesis", book_data)

# Or save individual chapters
for chapter in book_data["chapters"]:
    storage.save_chapter_data(
        "Genesis", 
        chapter["chapter"], 
        chapter
    )

# Export to CSV
all_verses = []
for chapter in book_data["chapters"]:
    all_verses.extend(chapter["verses"])

storage.save_verses_csv(all_verses, "Genesis_verses.csv")
    """)
    
    # Step 7: Close browser
    print("\nStep 7: Clean Up")
    print("-" * 80)
    print("""
playwright-browser_close()
print("Scraping complete!")
    """)
    
    print("\n" + "=" * 80)


def example_parser_usage():
    """Show how to use the HTML parser with scraped content."""
    
    print("\n" + "=" * 80)
    print("PARSER USAGE EXAMPLE")
    print("=" * 80)
    print()
    
    sample_html = """
    <div class="chapter">
        <p class="verse">
            <span class="v">1</span>
            In the beginning God created the heavens and the earth.
        </p>
        <p class="verse">
            <span class="v">2</span>
            Now the earth was formless and desolate...
        </p>
    </div>
    """
    
    print("Sample HTML content:")
    print(sample_html)
    print()
    
    print("Parsing code:")
    print("""
from src.parsers.html_parser import StudyBibleParser

# Create parser with HTML content
parser = StudyBibleParser(html_content)

# Extract all data
data = parser.parse_all()

# Access parsed data
print(f"Chapter: {data['chapter_info']}")
print(f"Verses: {len(data['verses'])}")

for verse in data['verses']:
    print(f"Verse {verse['number']}: {verse['text']}")
    """)


def example_storage_usage():
    """Show how to use the storage utilities."""
    
    print("\n" + "=" * 80)
    print("STORAGE USAGE EXAMPLE")
    print("=" * 80)
    print()
    
    print("""
from src.utils.storage import DataStorage

# Initialize storage
storage = DataStorage(base_dir='data')

# Sample chapter data
chapter_data = {
    "chapter": 1,
    "verses": [
        {"number": 1, "text": "In the beginning..."},
        {"number": 2, "text": "Now the earth..."}
    ],
    "study_notes": [
        {"id": "note1", "reference": "1:1", "content": "Study note..."}
    ]
}

# Save as JSON
storage.save_chapter_data("Genesis", 1, chapter_data)
# Saved to: data/raw/Genesis_chapter_1.json

# Load back
loaded_data = storage.load_json("Genesis_chapter_1.json")

# Export verses to CSV
storage.save_verses_csv(chapter_data["verses"], "genesis_ch1.csv")

# Get list of all saved books
saved_books = storage.get_all_saved_books()
print(f"Saved books: {saved_books}")
    """)


def example_error_handling():
    """Show error handling patterns."""
    
    print("\n" + "=" * 80)
    print("ERROR HANDLING EXAMPLE")
    print("=" * 80)
    print()
    
    print("""
import time
from typing import Optional

def scrape_with_retry(url: str, max_retries: int = 3) -> Optional[str]:
    '''Scrape with retry logic.'''
    
    for attempt in range(max_retries):
        try:
            # Navigate to URL
            playwright-browser_navigate(url=url)
            playwright-browser_wait_for(time=2)
            
            # Get snapshot
            snapshot = playwright-browser_snapshot()
            
            # Verify we got content
            if len(snapshot) < 100:
                raise ValueError("Snapshot too small, page may not have loaded")
            
            return snapshot
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            
            if attempt < max_retries - 1:
                # Wait before retry (exponential backoff)
                wait_time = 2 ** attempt
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("Max retries reached, giving up")
                return None
    
    return None


# Usage
snapshot = scrape_with_retry("https://www.jw.org/.../genesis/1/")
if snapshot:
    # Process snapshot
    pass
else:
    print("Failed to scrape page")
    """)


def example_batch_processing():
    """Show batch processing pattern."""
    
    print("\n" + "=" * 80)
    print("BATCH PROCESSING EXAMPLE")
    print("=" * 80)
    print()
    
    print("""
from src.config import BIBLE_BOOKS

def scrape_all_books():
    '''Scrape all 66 books of the Bible.'''
    
    storage = DataStorage()
    
    # Get list of all books
    all_books = []
    for testament, books in BIBLE_BOOKS.items():
        all_books.extend(books)
    
    # Process each book
    for book_info in all_books:
        print(f"Processing {book_info['name']}...")
        
        try:
            # Scrape all chapters in the book
            book_data = scrape_book(
                book_info['name'],
                book_info['chapters']
            )
            
            # Save book data
            storage.save_book_data(book_info['name'], book_data)
            
            print(f"✓ Completed {book_info['name']}")
            
        except Exception as e:
            print(f"✗ Failed {book_info['name']}: {e}")
            continue
        
        # Rate limiting between books
        time.sleep(10)
    
    print("All books processed!")


def scrape_book(book_name: str, chapter_count: int) -> dict:
    '''Scrape all chapters of a book.'''
    
    book_data = {
        "name": book_name,
        "chapters": []
    }
    
    for chapter_num in range(1, chapter_count + 1):
        print(f"  Chapter {chapter_num}/{chapter_count}")
        
        # Scrape chapter
        chapter_data = scrape_chapter(book_name, chapter_num)
        book_data["chapters"].append(chapter_data)
        
        # Rate limiting
        time.sleep(3)
    
    return book_data
    """)


def main():
    """Main function to run all examples."""
    
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 18 + "BIBLE SCRAPING INTEGRATION EXAMPLES" + " " * 25 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    examples = [
        ("1", "Complete Workflow", example_complete_workflow),
        ("2", "Parser Usage", example_parser_usage),
        ("3", "Storage Usage", example_storage_usage),
        ("4", "Error Handling", example_error_handling),
        ("5", "Batch Processing", example_batch_processing),
    ]
    
    print("Available examples:")
    for num, title, _ in examples:
        print(f"  {num}. {title}")
    print()
    
    choice = input("Select an example (1-5, or 'all'): ").strip().lower()
    print()
    
    if choice == 'all':
        for _, _, func in examples:
            func()
            print()
    elif choice in ['1', '2', '3', '4', '5']:
        idx = int(choice) - 1
        examples[idx][2]()
    else:
        print("Invalid choice. Running all examples...")
        for _, _, func in examples:
            func()
            print()
    
    print("\n" + "=" * 80)
    print("For more examples and documentation:")
    print("  - examples/playwright_mcp_guide.py - Playwright MCP tools guide")
    print("  - docs/PLAYWRIGHT_USAGE.md - Complete Playwright documentation")
    print("  - docs/GETTING_STARTED.md - Step-by-step setup guide")
    print("  - tests/test_playwright_scraper.py - Test examples")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
