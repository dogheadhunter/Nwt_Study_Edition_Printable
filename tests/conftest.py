"""
Pytest fixtures for Bible scraper tests.

This module provides shared fixtures for both unit and integration tests.
"""

import pytest
import os
import json
import socket
from pathlib import Path
from typing import Dict, Any

# Import scraper classes
from src.scrapers.psalms_scraper import Psalms83Scraper


@pytest.fixture
def data_dir():
    """Return the data directory path."""
    return Path(__file__).parent.parent / "data"


@pytest.fixture
def samples_dir(data_dir):
    """Return the samples directory path."""
    return data_dir / "samples"


@pytest.fixture
def psalms_83_sample(samples_dir):
    """Load Psalms 83 sample data."""
    sample_file = samples_dir / "psalms_83_sample.json"
    
    if sample_file.exists():
        with open(sample_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        pytest.skip("Sample data file not found")


@pytest.fixture
def psalms_scraper(tmp_path):
    """Create a Psalms83Scraper instance with temporary data directory."""
    return Psalms83Scraper(data_dir=str(tmp_path))


@pytest.fixture
def psalms_scraper_real():
    """Create a Psalms83Scraper instance with real data directory."""
    return Psalms83Scraper(data_dir="data")


def check_network_available(host: str = "www.jw.org", port: int = 443, timeout: int = 3) -> bool:
    """
    Check if network is available by attempting to connect to a host.
    
    Args:
        host: Hostname to check
        port: Port to connect to
        timeout: Connection timeout in seconds
        
    Returns:
        True if connection successful, False otherwise
    """
    try:
        socket.create_connection((host, port), timeout=timeout)
        return True
    except (socket.timeout, socket.error, OSError):
        return False


@pytest.fixture
def network_available():
    """Check if network is available for integration tests."""
    return check_network_available()


@pytest.fixture
def skip_if_no_network(network_available):
    """Skip test if network is not available."""
    if not network_available:
        pytest.skip("Network not available - skipping integration test")


@pytest.fixture
def jw_org_available():
    """Check if JW.org specifically is accessible."""
    return check_network_available("www.jw.org", 443, timeout=5)


@pytest.fixture
def skip_if_jw_org_blocked(jw_org_available):
    """Skip test if JW.org is blocked or unavailable."""
    if not jw_org_available:
        pytest.skip("JW.org not accessible - may be blocked or down")


@pytest.fixture
def sample_verse_html():
    """Sample HTML for a single verse (for unit testing parsers)."""
    return """
    <p class="verse" data-pid="1">
        <span class="v">1</span>
        O God, do not be silent; Do not keep quiet or still, O Divine One.
        <a class="footnoteLink" data-fnid="fn1">*</a>
        <a class="b" data-xref="xref1">a</a>
    </p>
    """


@pytest.fixture
def sample_study_note_html():
    """Sample HTML for a study note (for unit testing parsers)."""
    return """
    <div class="studyNote" id="note_83_3">
        <span class="reference">83:3</span>
        <div class="content">
            <p>your treasured ones: Or "those you carefully guard; those you keep hidden." 
            This Hebrew term refers to things or people that are precious and carefully protected.</p>
        </div>
    </div>
    """


@pytest.fixture
def sample_chapter_html():
    """Sample HTML for a complete chapter (for unit testing)."""
    return """
    <html>
    <head><title>Psalm 83 - NWT Study Bible</title></head>
    <body>
        <div class="chapter">
            <h1>Psalm <span class="chapterNumber">83</span></h1>
            <p class="superscription">A song. A melody of Asaph.</p>
            
            <div class="verses">
                <p class="verse" data-pid="1">
                    <span class="v">1</span>
                    O God, do not be silent; Do not keep quiet or still, O Divine One.
                </p>
                <p class="verse" data-pid="2">
                    <span class="v">2</span>
                    For look! your enemies are in an uproar; Those who hate you act arrogantly.
                </p>
            </div>
            
            <div class="studyNotes">
                <div class="studyNote" id="note_83_1">
                    <span class="reference">83:1</span>
                    <div class="content">
                        <p>O God: This is a study note example.</p>
                    </div>
                </div>
            </div>
            
            <div class="footnotes">
                <div class="footnote" id="fn_83_8">
                    <p>Selah: A technical term of uncertain meaning.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """


@pytest.fixture
def expected_psalms_83_structure():
    """Expected structure for Psalms 83 data."""
    return {
        "book": "Psalms",
        "chapter": 83,
        "total_verses": 18,
        "has_superscription": True,
        "min_study_notes": 5,
        "has_selah_footnote": True,
        "key_verse_18_content": ["Jehovah", "Most High"],
    }


@pytest.fixture
def mock_playwright_html():
    """Mock HTML that would be returned from playwright-browser_evaluate."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <body>
        <article class="article">
            <header>
                <h1>Psalm 83</h1>
                <p class="themeScrp">A song. A melody of Asaph.</p>
            </header>
            <div class="bodyTxt">
                <div class="pGroup">
                    <p id="p1" data-pid="1" class="p">
                        <span class="verse"><span class="v">1 </span>O God, do not be silent;</span>
                    </p>
                </div>
            </div>
        </article>
    </body>
    </html>
    """


# Marker helpers for better test categorization
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "live: mark test as requiring live internet access"
    )
    config.addinivalue_line(
        "markers", "jw_org: mark test as requiring access to jw.org"
    )
    config.addinivalue_line(
        "markers", "playwright: mark test as using Playwright browser automation"
    )
