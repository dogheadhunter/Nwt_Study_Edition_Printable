"""
JW.org Study Bible Scraper

This module provides functionality to scrape the JW.org Study Bible,
including Bible text, study notes, footnotes, and cross-references.

Usage:
    python -m src.scrapers.bible_scraper
"""

import time
import logging
from typing import Dict, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BibleScraper:
    """
    Scraper for JW.org Study Bible content.
    
    This class uses Selenium for browser automation to handle
    JavaScript-rendered content and dynamic loading.
    """
    
    BASE_URL = "https://www.jw.org/en/library/bible/study-bible/books/"
    
    def __init__(self, headless: bool = True, wait_time: int = 10):
        """
        Initialize the scraper.
        
        Args:
            headless: Run browser in headless mode
            wait_time: Maximum wait time for elements (seconds)
        """
        self.headless = headless
        self.wait_time = wait_time
        self.driver = None
        
    def setup_driver(self):
        """Set up Selenium WebDriver."""
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        try:
            self.driver = webdriver.Chrome(options=options)
            logger.info("WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
            
    def close_driver(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")
            
    def get_books_list(self) -> List[Dict[str, str]]:
        """
        Retrieve the list of all Bible books.
        
        Returns:
            List of dictionaries containing book information
        """
        if not self.driver:
            self.setup_driver()
            
        logger.info(f"Fetching books list from {self.BASE_URL}")
        self.driver.get(self.BASE_URL)
        
        # Wait for page to load
        time.sleep(2)
        
        books = []
        
        try:
            # Wait for book elements to load
            WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.CLASS_NAME, "bookLink"))
            )
            
            # Parse page with BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Find all book links (this selector may need adjustment)
            book_elements = soup.find_all('a', class_='bookLink')
            
            for book in book_elements:
                book_data = {
                    'name': book.get_text(strip=True),
                    'url': book.get('href', ''),
                    'has_study_notes': 'gem' in book.get('class', [])
                }
                books.append(book_data)
                logger.debug(f"Found book: {book_data['name']}")
                
        except TimeoutException:
            logger.warning("Timeout waiting for books list to load")
        except Exception as e:
            logger.error(f"Error fetching books list: {e}")
            
        logger.info(f"Found {len(books)} books")
        return books
        
    def get_chapter_content(self, book_url: str, chapter: int) -> Dict:
        """
        Retrieve content for a specific chapter.
        
        Args:
            book_url: URL path to the book
            chapter: Chapter number
            
        Returns:
            Dictionary containing chapter content
        """
        if not self.driver:
            self.setup_driver()
            
        # Construct full URL
        full_url = f"{self.BASE_URL.rstrip('/')}{book_url}/{chapter}/"
        logger.info(f"Fetching chapter content from {full_url}")
        
        self.driver.get(full_url)
        time.sleep(2)
        
        chapter_data = {
            'chapter': chapter,
            'verses': [],
            'study_notes': [],
            'footnotes': []
        }
        
        try:
            # Wait for verse content to load
            WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.CLASS_NAME, "verse"))
            )
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Extract verses (selectors may need adjustment based on actual HTML)
            verses = soup.find_all('p', class_='verse')
            
            for verse in verses:
                verse_num = verse.find('span', class_='v')
                verse_text = verse.get_text(strip=True)
                
                if verse_num:
                    chapter_data['verses'].append({
                        'number': verse_num.get_text(strip=True),
                        'text': verse_text
                    })
                    
        except TimeoutException:
            logger.warning(f"Timeout waiting for chapter content: {full_url}")
        except Exception as e:
            logger.error(f"Error fetching chapter content: {e}")
            
        return chapter_data
        
    def scrape_book(self, book_name: str) -> Dict:
        """
        Scrape all content for a specific book.
        
        Args:
            book_name: Name of the book to scrape
            
        Returns:
            Dictionary containing all book content
        """
        logger.info(f"Starting to scrape book: {book_name}")
        
        # This is a placeholder implementation
        # Actual implementation would iterate through all chapters
        
        book_data = {
            'name': book_name,
            'chapters': []
        }
        
        return book_data
        
    def scrape_all(self) -> List[Dict]:
        """
        Scrape the entire Bible with study notes.
        
        Returns:
            List of all books with their content
        """
        logger.info("Starting full Bible scrape")
        
        try:
            self.setup_driver()
            books = self.get_books_list()
            
            all_content = []
            
            for book in books:
                logger.info(f"Scraping: {book['name']}")
                # Add delay to be respectful to the server
                time.sleep(3)
                
                book_content = self.scrape_book(book['name'])
                all_content.append(book_content)
                
        finally:
            self.close_driver()
            
        logger.info("Full Bible scrape completed")
        return all_content


def main():
    """Main entry point for the scraper."""
    scraper = BibleScraper(headless=True)
    
    try:
        # Example: Get list of books
        books = scraper.get_books_list()
        print(f"Found {len(books)} books")
        
        for book in books[:5]:  # Print first 5 books
            print(f"- {book['name']}: {book['url']}")
            
    finally:
        scraper.close_driver()


if __name__ == "__main__":
    main()
