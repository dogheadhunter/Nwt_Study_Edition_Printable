"""
Example script demonstrating how to analyze the JW.org webpage structure.

This script shows how to:
1. Inspect network requests
2. Identify HTML elements
3. Understand dynamic content loading
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def analyze_webpage_structure():
    """
    Analyze the structure of the JW.org Study Bible webpage.
    
    This function demonstrates how to:
    - Set up a browser for inspection
    - Navigate to the page
    - Inspect the DOM structure
    - Identify key elements
    """
    print("Setting up WebDriver...")
    options = webdriver.ChromeOptions()
    # Run in headless mode (set to False to see the browser)
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    try:
        driver = webdriver.Chrome(options=options)
        
        # Navigate to the main books page
        url = "https://www.jw.org/en/library/bible/study-bible/books/"
        print(f"\nNavigating to: {url}")
        driver.get(url)
        
        # Wait for page to load
        print("Waiting for page to load...")
        time.sleep(5)
        
        # Get page source
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        print("\n" + "="*80)
        print("PAGE STRUCTURE ANALYSIS")
        print("="*80)
        
        # Analyze page title
        title = soup.find('title')
        print(f"\nPage Title: {title.get_text() if title else 'Not found'}")
        
        # Find main content containers
        print("\n--- Main Content Containers ---")
        main_divs = soup.find_all('div', class_=lambda x: x and ('container' in x.lower() or 'main' in x.lower()))
        print(f"Found {len(main_divs)} main container divs")
        
        for i, div in enumerate(main_divs[:3], 1):
            classes = div.get('class', [])
            print(f"{i}. Classes: {', '.join(classes)}")
        
        # Find links (potential book links)
        print("\n--- Links Analysis ---")
        all_links = soup.find_all('a')
        print(f"Total links on page: {len(all_links)}")
        
        # Filter links that might be book links
        bible_links = [link for link in all_links if 'bible' in link.get('href', '').lower()]
        print(f"Links containing 'bible': {len(bible_links)}")
        
        if bible_links:
            print("\nFirst 5 Bible-related links:")
            for link in bible_links[:5]:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                print(f"  - {text[:50]}: {href[:80]}")
        
        # Look for specific classes that might indicate books
        print("\n--- Searching for Book Elements ---")
        book_classes = ['book', 'bookLink', 'bible-book', 'testament']
        for class_name in book_classes:
            elements = soup.find_all(class_=class_name)
            if elements:
                print(f"Elements with class '{class_name}': {len(elements)}")
        
        # Look for list structures
        print("\n--- List Structures ---")
        lists = soup.find_all(['ul', 'ol'])
        print(f"Found {len(lists)} lists")
        
        # Analyze data attributes
        print("\n--- Data Attributes Analysis ---")
        elements_with_data = soup.find_all(lambda tag: any(attr.startswith('data-') for attr in tag.attrs))
        print(f"Elements with data-* attributes: {len(elements_with_data)}")
        
        if elements_with_data:
            # Show unique data attributes
            data_attrs = set()
            for elem in elements_with_data[:50]:
                data_attrs.update([attr for attr in elem.attrs if attr.startswith('data-')])
            
            print("Sample data attributes found:")
            for attr in sorted(list(data_attrs)[:10]):
                print(f"  - {attr}")
        
        # Save page source for manual inspection
        output_file = "examples/page_source_sample.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(page_source)
        print(f"\n✓ Full page source saved to: {output_file}")
        
        print("\n" + "="*80)
        print("ANALYSIS COMPLETE")
        print("="*80)
        print("\nNext steps:")
        print("1. Review the saved HTML file to identify exact selectors")
        print("2. Use browser DevTools to inspect network requests")
        print("3. Update scraper selectors based on findings")
        
    except Exception as e:
        print(f"\nError during analysis: {e}")
        print("\nNote: This may fail if the website is not accessible or blocks automated requests.")
        
    finally:
        if 'driver' in locals():
            driver.quit()
            print("\nWebDriver closed.")


def inspect_chapter_page():
    """
    Analyze the structure of a chapter page.
    
    This demonstrates how chapter content is structured.
    """
    print("\n" + "="*80)
    print("CHAPTER PAGE ANALYSIS")
    print("="*80)
    
    print("\nThis function would navigate to a specific chapter")
    print("Example URL: https://www.jw.org/en/library/bible/study-bible/books/genesis/1/")
    print("\nKey elements to look for:")
    print("- Verse containers")
    print("- Verse numbers")
    print("- Study note indicators")
    print("- Footnote markers")
    print("- Cross-reference links")
    print("- Media elements")


def main():
    """Main entry point."""
    print("JW.org Study Bible - Webpage Structure Analysis")
    print("=" * 80)
    
    choice = input("\nWhat would you like to analyze?\n1. Books list page\n2. Chapter page structure\n\nChoice (1 or 2): ")
    
    if choice == '1':
        analyze_webpage_structure()
    elif choice == '2':
        inspect_chapter_page()
    else:
        print("Invalid choice. Please run again and select 1 or 2.")


if __name__ == "__main__":
    main()
