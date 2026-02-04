# Documentation Index

Welcome to the NWT Study Edition Bible Scraper documentation!

## Quick Start

1. **New to the project?** Start with [GETTING_STARTED.md](GETTING_STARTED.md)
2. **Want to use Playwright?** Read [PLAYWRIGHT_USAGE.md](PLAYWRIGHT_USAGE.md)
3. **Need to understand the website?** Check [WEBPAGE_STRUCTURE.md](WEBPAGE_STRUCTURE.md)
4. **Looking for data models?** See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## Documentation Files

### Essential Reading

#### [GETTING_STARTED.md](GETTING_STARTED.md)
**Complete setup and usage guide**
- Environment setup instructions
- Installing dependencies
- Step-by-step scraping workflow
- Testing and validation
- Troubleshooting common issues

**Best for:** First-time users, setup questions

#### [PLAYWRIGHT_USAGE.md](PLAYWRIGHT_USAGE.md) ⭐ Recommended
**Playwright MCP tools comprehensive guide**
- All available MCP tools explained
- Complete scraping workflows
- Code examples and patterns
- Parsing snapshots
- Best practices
- Troubleshooting guide

**Best for:** Understanding Playwright MCP, writing scrapers

### Reference Documentation

#### [WEBPAGE_STRUCTURE.md](WEBPAGE_STRUCTURE.md)
**Analysis of JW.org Study Bible structure**
- Page architecture and components
- Content types (verses, notes, footnotes)
- Technical implementation details
- Data extraction strategies
- Scraping considerations

**Best for:** Understanding target website, planning scrapers

#### [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
**Data models and API patterns**
- Complete data models (Book, Chapter, Verse, etc.)
- Expected URL patterns
- Response format examples
- Database schema recommendations
- Usage examples

**Best for:** Data modeling, storage design, API integration

### Project Reports

#### [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
**Complete project summary and implementation status**
- Overview of project architecture
- List of implemented features
- Testing status and results
- Technical stack details

#### [INTEGRATION_TEST_SUMMARY.md](INTEGRATION_TEST_SUMMARY.md)
**Psalms 83 integration testing summary**
- Test execution results
- Data extraction verification
- Cross-reference verse text extraction
- Sidebar structure analysis

#### [LIVE_SCRAPING_RESULTS.md](LIVE_SCRAPING_RESULTS.md)
**Live scraping session results**
- Verified CSS selectors
- HTML structure findings
- Workflow documentation

#### [SIDEBAR_ANALYSIS.md](SIDEBAR_ANALYSIS.md)
**Study materials sidebar structure**
- Cross-reference HTML layout
- JavaScript population mechanism
- Testing requirements

## Examples

### Code Examples

Located in the `examples/` directory:

#### [playwright_mcp_guide.py](../examples/playwright_mcp_guide.py)
Interactive guide to Playwright MCP tools. Shows:
- Scraping books list
- Scraping chapter content
- Taking screenshots
- Interactive actions
- Parsing snapshots

Run with: `python examples/playwright_mcp_guide.py`

#### [integration_example.py](../examples/integration_example.py)
Complete integration examples showing:
- End-to-end scraping workflow
- Parser usage
- Storage usage
- Error handling
- Batch processing

Run with: `python examples/integration_example.py`

#### [demo_live_cross_refs.py](../examples/demo_live_cross_refs.py)
Demonstration of cross-reference verse text extraction.

Run with: `python examples/demo_live_cross_refs.py`

#### [analyze_structure.py](../examples/analyze_structure.py)
Webpage structure analysis tool (legacy Selenium).

## Tests

Located in the `tests/` directory:

### [test_playwright_scraper.py](../tests/test_playwright_scraper.py)
- Unit tests for scraper components
- Integration tests (requires MCP environment)
- Data structure validation

Run tests: `pytest tests/ -v`

## Learning Path

### For Beginners

1. Read [GETTING_STARTED.md](GETTING_STARTED.md) - Get oriented
2. Review [WEBPAGE_STRUCTURE.md](WEBPAGE_STRUCTURE.md) - Understand the target
3. Follow [PLAYWRIGHT_USAGE.md](PLAYWRIGHT_USAGE.md) - Learn the tools
4. Run `examples/playwright_mcp_guide.py` - See it in action
5. Try `examples/integration_example.py` - Complete workflows

### For Developers

1. Check [PLAYWRIGHT_USAGE.md](PLAYWRIGHT_USAGE.md) - Tool reference
2. Review [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Data models
3. Study `src/scrapers/playwright_scraper.py` - Implementation
4. Review `tests/test_playwright_scraper.py` - Test patterns
5. Customize for your needs

### For Data Scientists

1. Read [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Data structure
2. Review [WEBPAGE_STRUCTURE.md](WEBPAGE_STRUCTURE.md) - Data sources
3. Check `src/utils/storage.py` - Storage utilities
4. Plan your analysis pipeline

## Quick Reference

### Key Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# View Playwright guide
python examples/playwright_mcp_guide.py

# View integration examples
python examples/integration_example.py
```

### Key Files

- **Scrapers**: `src/scrapers/playwright_scraper.py` (recommended)
- **Parsers**: `src/parsers/html_parser.py`
- **Storage**: `src/utils/storage.py`
- **Config**: `src/config.py`
- **Tests**: `tests/test_playwright_scraper.py`

### Playwright MCP Tools

Quick reference for most-used tools:

```python
# Navigate
playwright-browser_navigate(url="...")

# Wait
playwright-browser_wait_for(time=2)

# Inspect
snapshot = playwright-browser_snapshot()

# Click
playwright-browser_click(element="...", ref="...")

# Screenshot
playwright-browser_take_screenshot(filename="...")

# Close
playwright-browser_close()
```

See [PLAYWRIGHT_USAGE.md](PLAYWRIGHT_USAGE.md) for complete reference.

## Common Questions

### How do I get started?
→ Read [GETTING_STARTED.md](GETTING_STARTED.md)

### What's the difference between Playwright and Selenium?
→ See "Comparison with Selenium" in [PLAYWRIGHT_USAGE.md](PLAYWRIGHT_USAGE.md)

### How do I scrape a specific book?
→ Check the examples in [PLAYWRIGHT_USAGE.md](PLAYWRIGHT_USAGE.md) or run `examples/integration_example.py`

### What data can I extract?
→ See data models in [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

### Why is the website blocking me?
→ See "Troubleshooting" in [PLAYWRIGHT_USAGE.md](PLAYWRIGHT_USAGE.md)

### How do I parse the snapshots?
→ See "Parsing Snapshots" section in [PLAYWRIGHT_USAGE.md](PLAYWRIGHT_USAGE.md)

## Contributing

Found an issue or want to contribute?

1. Check existing documentation
2. Review code examples
3. Run tests to verify your changes
4. Update documentation if needed

## Support

Need help?

1. **Documentation**: Check this index and linked docs
2. **Examples**: Run the example scripts
3. **Tests**: Review test cases for patterns
4. **Issues**: Open a GitHub issue with details

## Additional Resources

- [Playwright Official Docs](https://playwright.dev/)
- [Model Context Protocol](https://modelcontextprotocol.org/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/)
- [pytest Documentation](https://docs.pytest.org/)

---

**Last Updated**: 2026-02-04

**Version**: 1.0 (Playwright MCP Migration)
