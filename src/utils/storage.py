"""
Data Storage Utilities

This module provides utilities for saving and loading scraped data
in various formats (JSON, CSV, etc.).
"""

import json
import csv
import os
from typing import Dict, List, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataStorage:
    """Handle storage of scraped Bible data."""
    
    def __init__(self, base_dir: str = 'data'):
        """
        Initialize data storage.
        
        Args:
            base_dir: Base directory for storing data
        """
        self.base_dir = base_dir
        self.raw_dir = os.path.join(base_dir, 'raw')
        self.processed_dir = os.path.join(base_dir, 'processed')
        
        # Create directories if they don't exist
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
        
    def save_json(self, data: Dict[str, Any], filename: str, processed: bool = False) -> str:
        """
        Save data as JSON file.
        
        Args:
            data: Dictionary to save
            filename: Name of the file
            processed: Whether this is processed data
            
        Returns:
            Path to saved file
        """
        directory = self.processed_dir if processed else self.raw_dir
        filepath = os.path.join(directory, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved JSON data to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving JSON: {e}")
            raise
            
    def load_json(self, filename: str, processed: bool = False) -> Dict[str, Any]:
        """
        Load data from JSON file.
        
        Args:
            filename: Name of the file
            processed: Whether this is processed data
            
        Returns:
            Loaded dictionary
        """
        directory = self.processed_dir if processed else self.raw_dir
        filepath = os.path.join(directory, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Loaded JSON data from {filepath}")
            return data
        except Exception as e:
            logger.error(f"Error loading JSON: {e}")
            raise
            
    def save_verses_csv(self, verses: List[Dict[str, str]], filename: str) -> str:
        """
        Save verses as CSV file.
        
        Args:
            verses: List of verse dictionaries
            filename: Name of the file
            
        Returns:
            Path to saved file
        """
        filepath = os.path.join(self.processed_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                if verses:
                    writer = csv.DictWriter(f, fieldnames=verses[0].keys())
                    writer.writeheader()
                    writer.writerows(verses)
            logger.info(f"Saved CSV data to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving CSV: {e}")
            raise
            
    def save_book_data(self, book_name: str, book_data: Dict[str, Any]) -> str:
        """
        Save data for a complete book.
        
        Args:
            book_name: Name of the book
            book_data: Complete book data
            
        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{book_name.replace(' ', '_')}_{timestamp}.json"
        return self.save_json(book_data, filename, processed=False)
        
    def save_chapter_data(self, book_name: str, chapter: int, chapter_data: Dict[str, Any]) -> str:
        """
        Save data for a specific chapter.
        
        Args:
            book_name: Name of the book
            chapter: Chapter number
            chapter_data: Chapter data
            
        Returns:
            Path to saved file
        """
        filename = f"{book_name.replace(' ', '_')}_chapter_{chapter}.json"
        return self.save_json(chapter_data, filename, processed=False)
        
    def get_all_saved_books(self) -> List[str]:
        """
        Get list of all saved book files.
        
        Returns:
            List of filenames
        """
        files = [f for f in os.listdir(self.raw_dir) if f.endswith('.json')]
        return files
