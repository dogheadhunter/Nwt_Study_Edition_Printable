"""
Example: Using Playwright MCP Tools for Bible Scraping

This script demonstrates how to use Playwright MCP tools to scrape
the JW.org Study Bible. This is a documentation/guide script showing
the workflow.

Note: This script documents the MCP tool usage pattern. In the actual
MCP environment, you would call these tools directly through the MCP interface.
"""


def example_scrape_books_list():
    """
    Example workflow for scraping the books list.
    
    This demonstrates the Playwright MCP tools workflow.
    """
    print("=" * 80)
    print("EXAMPLE: Scraping Books List with Playwright MCP")
    print("=" * 80)
    print()
    
    workflow = [
        {
            "step": 1,
            "tool": "playwright-browser_navigate",
            "params": {
                "url": "https://www.jw.org/en/library/bible/study-bible/books/"
            },
            "description": "Navigate to the books list page"
        },
        {
            "step": 2,
            "tool": "playwright-browser_wait_for",
            "params": {
                "time": 2
            },
            "description": "Wait for page to fully load"
        },
        {
            "step": 3,
            "tool": "playwright-browser_snapshot",
            "params": {},
            "description": "Get accessibility snapshot of the page"
        },
        {
            "step": 4,
            "action": "Parse snapshot",
            "description": "Look for book links in the snapshot output"
        },
        {
            "step": 5,
            "action": "Extract data",
            "description": "Extract book names and URLs from identified elements"
        },
        {
            "step": 6,
            "tool": "playwright-browser_close",
            "params": {},
            "description": "Close the browser"
        }
    ]
    
    for item in workflow:
        print(f"Step {item['step']}: {item['description']}")
        if 'tool' in item:
            print(f"  Tool: {item['tool']}")
            print(f"  Params: {item.get('params', {})}")
        else:
            print(f"  Action: {item.get('action', 'N/A')}")
        print()


def example_scrape_chapter():
    """
    Example workflow for scraping a specific chapter.
    """
    print("=" * 80)
    print("EXAMPLE: Scraping Genesis Chapter 1 with Playwright MCP")
    print("=" * 80)
    print()
    
    workflow = [
        {
            "step": 1,
            "tool": "playwright-browser_navigate",
            "params": {
                "url": "https://www.jw.org/en/library/bible/study-bible/books/genesis/1/"
            },
            "description": "Navigate to Genesis chapter 1"
        },
        {
            "step": 2,
            "tool": "playwright-browser_wait_for",
            "params": {
                "time": 3
            },
            "description": "Wait for chapter content to load (including JS)"
        },
        {
            "step": 3,
            "tool": "playwright-browser_snapshot",
            "params": {},
            "description": "Get page structure"
        },
        {
            "step": 4,
            "action": "Identify elements",
            "description": "From snapshot, identify: verses, verse numbers, study note markers"
        },
        {
            "step": 5,
            "action": "Click study note",
            "description": "Optional: Click on a study note marker to reveal note panel"
        },
        {
            "step": 5.1,
            "tool": "playwright-browser_click",
            "params": {
                "element": "Study note marker",
                "ref": "<ref from snapshot>"
            },
            "description": "Click to reveal study note"
        },
        {
            "step": 5.2,
            "tool": "playwright-browser_wait_for",
            "params": {
                "time": 1
            },
            "description": "Wait for study pane to appear"
        },
        {
            "step": 5.3,
            "tool": "playwright-browser_snapshot",
            "params": {},
            "description": "Get updated snapshot with study note visible"
        },
        {
            "step": 6,
            "action": "Extract and structure data",
            "description": "Parse verses, notes, footnotes from snapshots"
        },
        {
            "step": 7,
            "tool": "playwright-browser_close",
            "params": {},
            "description": "Close browser"
        }
    ]
    
    for item in workflow:
        step_num = item['step']
        print(f"Step {step_num}: {item['description']}")
        if 'tool' in item:
            print(f"  Tool: {item['tool']}")
            print(f"  Params: {item.get('params', {})}")
        else:
            print(f"  Action: {item.get('action', 'N/A')}")
        print()


def example_take_screenshot():
    """
    Example: Taking screenshots for documentation.
    """
    print("=" * 80)
    print("EXAMPLE: Taking Screenshots")
    print("=" * 80)
    print()
    
    workflow = [
        {
            "step": 1,
            "tool": "playwright-browser_navigate",
            "params": {
                "url": "https://www.jw.org/en/library/bible/study-bible/books/"
            }
        },
        {
            "step": 2,
            "tool": "playwright-browser_take_screenshot",
            "params": {
                "filename": "books_list.png",
                "fullPage": True
            },
            "description": "Take full page screenshot"
        },
        {
            "step": 3,
            "tool": "playwright-browser_close",
            "params": {}
        }
    ]
    
    for item in workflow:
        print(f"Step {item['step']}: {item.get('description', 'Execute tool')}")
        if 'tool' in item:
            print(f"  Tool: {item['tool']}")
        print()


def example_interactive_scraping():
    """
    Example: Interactive scraping with form filling or clicking.
    """
    print("=" * 80)
    print("EXAMPLE: Interactive Scraping")
    print("=" * 80)
    print()
    
    print("Playwright MCP supports interactive actions:")
    print()
    
    actions = [
        "playwright-browser_click - Click buttons, links, or elements",
        "playwright-browser_type - Type text into input fields",
        "playwright-browser_select_option - Select from dropdowns",
        "playwright-browser_hover - Hover over elements (for tooltips, etc.)",
        "playwright-browser_press_key - Press keyboard keys",
    ]
    
    for action in actions:
        print(f"  • {action}")
    print()
    
    print("These are useful for:")
    print("  - Navigating multi-page content")
    print("  - Revealing hidden study notes or footnotes")
    print("  - Interacting with chapter/verse selectors")
    print("  - Handling dynamic content loading")
    print()


def show_snapshot_parsing_example():
    """
    Show how to parse Playwright snapshot output.
    """
    print("=" * 80)
    print("EXAMPLE: Parsing Snapshot Output")
    print("=" * 80)
    print()
    
    print("Playwright snapshot returns an accessibility tree like:")
    print()
    print("```")
    print('heading "New World Translation Study Bible"')
    print('  link "Genesis"')
    print('  link "Exodus"')
    print('  link "Leviticus"')
    print('  ...')
    print("```")
    print()
    print("To extract books, parse lines containing 'link' elements")
    print("and extract the text within quotes.")
    print()
    
    sample_code = '''
def parse_books_from_snapshot(snapshot_text):
    """Extract book names from snapshot."""
    books = []
    for line in snapshot_text.split('\\n'):
        if 'link' in line.lower() and '"' in line:
            # Extract text between quotes
            start = line.find('"') + 1
            end = line.find('"', start)
            if end > start:
                book_name = line[start:end]
                books.append(book_name)
    return books
'''
    
    print("Example parsing function:")
    print(sample_code)


def main():
    """Main function to display all examples."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "PLAYWRIGHT MCP SCRAPING GUIDE" + " " * 29 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    examples = [
        ("1", "Scrape Books List", example_scrape_books_list),
        ("2", "Scrape Chapter Content", example_scrape_chapter),
        ("3", "Take Screenshots", example_take_screenshot),
        ("4", "Interactive Actions", example_interactive_scraping),
        ("5", "Parse Snapshots", show_snapshot_parsing_example),
    ]
    
    print("Available examples:")
    for num, title, _ in examples:
        print(f"  {num}. {title}")
    print()
    
    choice = input("Select an example (1-5, or 'all' for all): ").strip().lower()
    print()
    
    if choice == 'all':
        for _, _, func in examples:
            func()
            print()
    elif choice in ['1', '2', '3', '4', '5']:
        idx = int(choice) - 1
        examples[idx][2]()
    else:
        print("Invalid choice. Running all examples...\n")
        for _, _, func in examples:
            func()
            print()
    
    print("=" * 80)
    print("For more information, see:")
    print("  - docs/PLAYWRIGHT_USAGE.md")
    print("  - tests/test_playwright_scraper.py")
    print("=" * 80)


if __name__ == "__main__":
    main()
