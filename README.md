# NWT Study Edition - Bible Scraping Repository

A repository for understanding and scraping the JW.org Study Bible (New World Translation Study Edition), including Bible text, study notes, footnotes, cross-references, and additional study materials.

## Overview

This project provides tools and documentation to:
- Understand how the JW.org Study Bible webpage is structured
- Scrape the complete Bible text with study notes
- Extract and organize footnotes, cross-references, and media content
- Store the data in structured formats for further use

## Project Structure

```
Nwt_Study_Edition_Printable/
├── docs/                      # Documentation
│   ├── WEBPAGE_STRUCTURE.md   # Analysis of JW.org webpage structure
│   └── API_DOCUMENTATION.md   # Data models and API patterns
├── src/                       # Source code
│   ├── scrapers/              # Web scraping modules
│   │   └── bible_scraper.py   # Main scraper for JW.org content
│   ├── parsers/               # HTML parsing utilities
│   │   └── html_parser.py     # Parse and extract structured data
│   └── utils/                 # Utility functions
│       └── storage.py         # Data storage utilities
├── examples/                  # Example scripts
│   └── analyze_structure.py   # Script to analyze webpage structure
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Features

### Web Scraping
- **Browser Automation**: Uses Selenium to handle JavaScript-rendered content
- **Dynamic Content**: Captures study notes and cross-references loaded via AJAX
- **Rate Limiting**: Implements respectful delays between requests
- **Error Handling**: Robust error handling for network and parsing issues

### Data Extraction
- **Verses**: Complete Bible text with verse numbers
- **Study Notes**: Detailed commentary on verses
- **Footnotes**: Translation notes and definitions
- **Cross-References**: Links between related verses
- **Media**: Images, videos, and audio content

### Data Storage
- **JSON Format**: Structured data storage
- **CSV Export**: Tabular format for verses
- **Organized Structure**: Separate files for books and chapters

## Installation

### Prerequisites
- Python 3.8 or higher
- Chrome browser (for Selenium WebDriver)
- ChromeDriver (will be installed automatically)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/dogheadhunter/Nwt_Study_Edition_Printable.git
cd Nwt_Study_Edition_Printable
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Analyzing the Webpage Structure

Before scraping, analyze the webpage structure to understand the HTML elements:

```bash
python examples/analyze_structure.py
```

This will:
- Inspect the main books page
- Identify HTML elements and classes
- Save a sample of the page source for manual review

### Scraping Bible Content

#### Get List of Books
```python
from src.scrapers.bible_scraper import BibleScraper

scraper = BibleScraper(headless=True)
books = scraper.get_books_list()

for book in books:
    print(f"{book['name']}: {book['url']}")
    
scraper.close_driver()
```

#### Scrape a Chapter
```python
from src.scrapers.bible_scraper import BibleScraper
from src.utils.storage import DataStorage

scraper = BibleScraper(headless=True)
storage = DataStorage()

# Get chapter content
chapter_data = scraper.get_chapter_content('/genesis', 1)

# Save the data
storage.save_chapter_data('Genesis', 1, chapter_data)

scraper.close_driver()
```

#### Parse HTML Content
```python
from src.parsers.html_parser import StudyBibleParser

# Parse HTML file
parser = StudyBibleParser(html_content)
data = parser.parse_all()

# Access structured data
print(f"Chapter: {data['chapter_info']}")
print(f"Verses: {len(data['verses'])}")
print(f"Study Notes: {len(data['study_notes'])}")
```

## Documentation

### Webpage Structure
See [docs/WEBPAGE_STRUCTURE.md](docs/WEBPAGE_STRUCTURE.md) for detailed analysis of:
- Page architecture and components
- Content types and organization
- Technical implementation details
- Scraping strategies

### API Documentation
See [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for:
- Data models and schemas
- Expected URL patterns
- Response formats
- Database structure recommendations

## Important Notes

### Legal and Ethical Considerations

⚠️ **Copyright Notice**: The New World Translation and all study materials are copyrighted by the Watchtower Bible and Tract Society. This repository is for educational purposes to understand web scraping techniques and webpage structures.

Before using this tool:
1. Review JW.org's Terms of Service
2. Respect copyright and intellectual property rights
3. Implement appropriate rate limiting
4. Do not use scraped content for commercial purposes
5. Consider reaching out to JW.org for official API access

### Rate Limiting
The scraper implements delays between requests to be respectful to the server:
- Default: 2-3 seconds between requests
- Adjustable via scraper settings
- Consider longer delays for bulk scraping

### Reliability
- HTML structure may change; selectors may need updates
- Some content may be loaded dynamically and require additional waits
- Network issues may require retry logic

## Development

### Project Status
This is an educational repository demonstrating:
- Web scraping techniques for dynamic content
- HTML parsing and data extraction
- Structured data storage

### Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### TODO
- [ ] Verify HTML selectors with actual webpage
- [ ] Implement retry logic for failed requests
- [ ] Add progress tracking for bulk scraping
- [ ] Create database schema implementation
- [ ] Add export to different formats (PDF, EPUB)
- [ ] Implement caching layer
- [ ] Add unit tests

## Technical Stack

- **Python 3.8+**: Core language
- **Selenium**: Browser automation for JavaScript content
- **BeautifulSoup4**: HTML parsing
- **lxml**: Fast XML/HTML processing
- **Requests**: HTTP library (for static content)

## License

This project is for educational purposes. All Bible content and study materials are copyrighted by the Watchtower Bible and Tract Society.

## Disclaimer

This tool is not affiliated with or endorsed by JW.org or the Watchtower Bible and Tract Society. It is an independent educational project for understanding web scraping techniques.

## Support

For issues or questions:
1. Check the documentation in the `docs/` directory
2. Review existing issues on GitHub
3. Open a new issue with detailed information

## Acknowledgments

- JW.org for providing the Study Bible online
- The Python community for excellent libraries
- Contributors to this project
