# GitHub Copilot Setup Guide

This guide will help you set up and use GitHub Copilot's custom instructions, agent profiles, and MCP (Model Context Protocol) servers for the NWT Study Edition Printable project.

## Prerequisites

Before you begin, ensure you have:

- **VS Code**: Version 1.102 or later
- **GitHub Copilot**: Active subscription and VS Code extension installed
- **Node.js**: Version 18 or later (for MCP servers)
- **Python**: Version 3.8 or later
- **Git**: For repository access

### Required VS Code Extensions

1. **GitHub Copilot** (`GitHub.copilot`)
2. **GitHub Copilot Chat** (`GitHub.copilot-chat`)
3. **Python** (`ms-python.python`)

Install these from the VS Code Extensions marketplace if you haven't already.

## Quick Setup

### 1. Enable Agent Mode

1. Open VS Code Settings (File > Preferences > Settings)
2. Search for "Copilot Agent"
3. Enable the following settings:
   - `github.copilot.chat.agentMode`: ✓ Enabled
   - `chat.agent.enabled`: ✓ Enabled
   - `github.copilot.advanced.customAgents`: ✓ Enabled

Alternatively, these are already configured in `.vscode/settings.json` and will be applied automatically when you open this workspace.

### 2. Configure GitHub Personal Access Token (PAT)

The MCP GitHub server requires a Personal Access Token:

1. Go to GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
2. Click "Generate new token (classic)"
3. Name it "Copilot MCP GitHub Access"
4. Select scopes:
   - ✓ `repo` (Full control of private repositories)
   - ✓ `workflow` (Update GitHub Action workflows)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)

When you first use an MCP tool that needs GitHub access, VS Code will prompt you for this token.

### 3. Install Node.js Dependencies

The MCP servers run via npx, which will automatically download them when first used. No manual installation needed!

However, to verify your Node.js setup:

```bash
node --version  # Should be v18 or higher
npx --version   # Should be installed with Node.js
```

### 4. Verify Setup

1. Open VS Code in this repository
2. Open GitHub Copilot Chat (Ctrl+Alt+I or Cmd+Alt+I)
3. Type `@workspace` - you should see custom agents appear
4. Try invoking an agent: `@planner create a plan for scraping Genesis`

## Using Custom Agents

### Available Agents

| Agent | Symbol | Purpose | Key Use Cases |
|-------|--------|---------|---------------|
| **planner** | 📋 | Plans and breaks down tasks | Creating implementation plans, analyzing requirements |
| **scraper** | 🕸️ | Web scraping with Playwright MCP | Scraping JW.org pages, extracting HTML |
| **parser** | 📄 | HTML parsing with BeautifulSoup | Extracting verses, study notes, footnotes |
| **tester** | 🧪 | Writing pytest tests | Creating unit tests, mocking, fixtures |
| **docs** | 📚 | Technical documentation | Writing guides, docstrings, README updates |
| **reviewer** | 👀 | Code review | Reviewing code quality, security, best practices |

### Invoking Agents

In GitHub Copilot Chat, use the `@` symbol followed by the agent name:

```
@planner Create a plan to scrape the book of Genesis
@scraper Scrape Genesis chapter 1
@parser Extract verses from this HTML: <html>...</html>
@tester Create tests for the verse extraction function
@docs Document the scrape_chapter function
@reviewer Review my recent changes to the scraper
```

### Agent Workflow with Handoffs

The agents are designed to work together through handoffs:

```
┌──────────────┐
│   PLANNER    │  1. Start here: Break down task
│    Agent     │
└──────┬───────┘
       │
       ├──────────────────────────────────────┐
       │                                      │
       ▼                                      ▼
┌──────────────┐                      ┌──────────────┐
│   SCRAPER    │  2. Implement        │    PARSER    │  2. Or parse
│    Agent     │     scraping         │    Agent     │     HTML
└──────┬───────┘                      └──────┬───────┘
       │                                      │
       └──────────────┬───────────────────────┘
                      │
                      ▼
               ┌──────────────┐
               │    TESTER    │  3. Write tests
               │    Agent     │
               └──────┬───────┘
                      │
                      ▼
               ┌──────────────┐
               │   REVIEWER   │  4. Code review
               │    Agent     │
               └──────┬───────┘
                      │
                      ▼
               ┌──────────────┐
               │     DOCS     │  5. Document
               │    Agent     │
               └──────────────┘
```

**Example Workflow:**

1. **Start with planner**: `@planner I need to scrape all chapters of Genesis`
2. **Planner creates a detailed plan and offers handoff buttons**
3. **Click "🕸️ Start Scraping Implementation"** to hand off to scraper agent
4. **Scraper implements and offers handoff** to parser or tester
5. **Continue the workflow** through testing, review, and documentation

## MCP Server Details

### What is MCP?

Model Context Protocol (MCP) is a standard for connecting AI assistants to external tools and data sources. This project uses three MCP servers:

1. **Playwright MCP**: Browser automation for web scraping
2. **GitHub MCP**: GitHub API access for repository operations
3. **Filesystem MCP**: Safe file system access within the workspace

### Playwright MCP Server

**Purpose**: Provides browser automation tools for web scraping.

**Available Tools**:
- `playwright-browser_navigate`: Navigate to URLs
- `playwright-browser_snapshot`: Get page structure
- `playwright-browser_click`: Click elements
- `playwright-browser_wait_for`: Wait for content
- `playwright-browser_evaluate`: Execute JavaScript
- `playwright-browser_take_screenshot`: Capture screenshots
- `playwright-browser_close`: Clean up browser

**Usage Example**:
```
@scraper Navigate to https://www.jw.org/en/library/bible/study-bible/books/ and list all Bible books
```

### GitHub MCP Server

**Purpose**: Access GitHub API for repository operations.

**Available Tools**:
- List issues, pull requests, branches
- Get file contents
- View workflow runs
- Search code
- And more...

**Usage Example**:
```
@workspace Show me recent issues in this repository
```

**Setup**: Requires GitHub Personal Access Token (see Quick Setup section above).

### Filesystem MCP Server

**Purpose**: Safe file system access scoped to the workspace.

**Scope**: Limited to `${workspaceFolder}` - cannot access files outside the project.

**Usage**: Automatically used by agents when reading/writing files.

## Troubleshooting

### Agent Not Found

**Problem**: Typing `@planner` doesn't show the agent.

**Solutions**:
1. Verify `.github/agents/planner.agent.md` exists
2. Check that agent mode is enabled in settings
3. Reload VS Code window (Ctrl+Shift+P > "Reload Window")
4. Update VS Code to latest version

### MCP Server Won't Start

**Problem**: Error message about MCP server failing to start.

**Solutions**:
1. Check Node.js version: `node --version` (need v18+)
2. Clear npx cache: `npx clear-npx-cache`
3. Check VS Code output panel: View > Output > Select "MCP" from dropdown
4. Restart VS Code

### GitHub PAT Issues

**Problem**: GitHub MCP asks for token repeatedly or shows authentication error.

**Solutions**:
1. Verify token has correct scopes (`repo`, `workflow`)
2. Token might be expired - generate a new one
3. Check token in VS Code settings
4. Clear and re-enter the token when prompted

### Playwright Tools Not Working

**Problem**: Playwright browser tools fail or timeout.

**Solutions**:
1. Check internet connection
2. Verify Node.js is installed
3. First run may take time to download Playwright
4. Check VS Code output panel for specific errors

### Agent Doesn't Follow Instructions

**Problem**: Agent provides generic responses instead of project-specific help.

**Solutions**:
1. Be more specific in your request
2. Reference specific files or functions
3. Provide context from the codebase
4. Use handoffs to ensure the right agent is working
5. Check that `.github/copilot-instructions.md` exists

## File Locations Reference

### Configuration Files
```
.github/
├── copilot-instructions.md          # Project-wide Copilot instructions
└── agents/                          # Agent profile definitions
    ├── planner.agent.md
    ├── scraper.agent.md
    ├── parser.agent.md
    ├── tester.agent.md
    ├── docs.agent.md
    └── reviewer.agent.md

.vscode/
├── settings.json                    # VS Code and Copilot settings
└── mcp.json                         # MCP server configuration
```

### Key Documentation
```
docs/
├── COPILOT_SETUP.md                 # This file
├── GETTING_STARTED.md               # Project setup guide
├── PLAYWRIGHT_USAGE.md              # Playwright MCP usage
├── API_DOCUMENTATION.md             # Data models and patterns
└── WEBPAGE_STRUCTURE.md             # HTML structure analysis
```

## Best Practices

### When to Use Which Agent

- **@planner**: Starting a new feature, breaking down complex tasks
- **@scraper**: Implementing web scraping, browser automation
- **@parser**: Extracting data from HTML, data transformation
- **@tester**: Writing tests, creating fixtures, mocking
- **@docs**: Writing documentation, docstrings, guides
- **@reviewer**: Code review, finding issues, security check

### Effective Agent Prompts

✅ **Good Prompts** (specific, contextual):
```
@planner Create a plan to add cross-reference extraction to the parser
@scraper Use Playwright MCP to scrape Genesis chapter 1 from JW.org
@tester Create pytest tests for the extract_verses function in src/parsers/html_parser.py
@docs Add docstrings to all functions in src/utils/storage.py
@reviewer Review the changes in src/scrapers/playwright_scraper.py for rate limiting issues
```

❌ **Vague Prompts** (too general):
```
@planner Help me
@scraper Scrape something
@tester Make tests
@docs Write docs
@reviewer Check my code
```

### Using Handoffs Effectively

1. **Let agents complete their work** before manually modifying
2. **Follow the suggested workflow** (plan → implement → test → review → document)
3. **Use handoff buttons** in the chat interface when offered
4. **Provide context** when accepting a handoff

## Next Steps

Now that you have Copilot set up:

1. **Try the workflow**: 
   ```
   @planner Create a plan to scrape Matthew chapter 5
   ```

2. **Explore the agents**:
   - Ask each agent what they can do
   - Try different types of requests
   - Use handoffs between agents

3. **Read the documentation**:
   - [Getting Started Guide](./GETTING_STARTED.md)
   - [Playwright Usage Guide](./PLAYWRIGHT_USAGE.md)
   - [API Documentation](./API_DOCUMENTATION.md)

4. **Start scraping**:
   ```python
   @scraper Show me how to scrape the books list page
   ```

5. **Write tests**:
   ```python
   @tester Create test fixtures for sample Bible verses
   ```

## Additional Resources

### GitHub Copilot Documentation
- [GitHub Copilot Docs](https://docs.github.com/en/copilot)
- [Custom Instructions Guide](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)
- [Agent Mode Documentation](https://code.visualstudio.com/docs/copilot/copilot-chat)

### MCP Protocol
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Playwright MCP Server](https://github.com/executeautomation/playwright-mcp-server)
- [GitHub MCP Server](https://github.com/modelcontextprotocol/servers)

### Project-Specific
- [Project README](../README.md)
- [Contributing Guidelines](../CONTRIBUTING.md) (if exists)
- [Issue Tracker](https://github.com/dogheadhunter/Nwt_Study_Edition_Printable/issues)

## Support

If you encounter issues:

1. Check this guide's Troubleshooting section
2. Review the VS Code Output panel (View > Output)
3. Check existing GitHub issues
4. Open a new issue with:
   - VS Code version
   - Node.js version
   - Error messages from Output panel
   - Steps to reproduce

## License and Legal

This project is for educational purposes. All Bible content is copyrighted by the Watchtower Bible and Tract Society. See [README](../README.md) for full details.

---

**Happy Coding with GitHub Copilot! 🚀**
