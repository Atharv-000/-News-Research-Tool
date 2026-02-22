# Equity Research News Tool

An end-to-end news research tool using LangChain, OpenAI API, and NewsAPI. Enter a query to fetch relevant news articles and receive an AI-powered summary suitable for equity research analysis.

## Features

- **News fetching**: Retrieves latest news from NewsAPI based on your search query
- **AI summarization**: Uses OpenAI (GPT-3.5) to provide concise, professional summaries
- **CLI interface**: Command-line tool you can extend with your own UI/UX (web, desktop, etc.)

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Obtain API keys

- **OpenAI API key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- **NewsAPI key**: Get from [NewsAPI.org](https://newsapi.org/register)

### 3. Configure environment

Create a `.env` file in the project root (or copy from `.env.example`):

```
OPENAI_API_KEY=your-openai-api-key
NEWSAPI_KEY=your-newsapi-key
```

## Usage

### Web app (text + source links)

```bash
python web_app.py
```

Then open `http://127.0.0.1:5000` in your browser, enter a query, and you’ll see article text plus links to the full news pages.

### CLI (one-shot, query as argument)

```bash
python app.py "Tesla stock"
```

### CLI (interactive mode, multiple queries)

```bash
python app.py
```

Then type your query when prompted. Press Enter on an empty line or Ctrl+C to quit.

### Direct config run (default query)

```bash
python langchain_config.py
```

Runs a default query ("equity market trends") and prints the summary.

## Project structure

```
News Research Tool/
├── app.py              # CLI entry point (extend with your own UI)
├── web_app.py          # Flask web app (text + links)
├── langchain_config.py # LangChain setup, NewsAPI integration, LLM chain
├── requirements.txt    # Python dependencies
├── .env                # API keys (create from .env.example)
├── .env.example        # Template for environment variables
└── README.md           # This file
```

## Adding your own UI

The logic is separated for easy integration:

```python
from langchain_config import llm_chain, get_summary

# Fetch raw news summaries
summaries = get_summary("your query")

# Get AI summary (or handle exceptions)
result = llm_chain.invoke({"query": "your query", "summaries": summaries})
```

Or use the CLI helper:

```python
from app import run_query
summary = run_query("Tesla stock")
```

## Workflow

1. User enters a query (CLI or your custom UI)
2. NewsAPI fetches relevant English news articles (sorted by relevancy)
3. Article descriptions/titles are combined into a single text
4. LangChain sends the query + article text to OpenAI for summarization
5. The AI returns a concise professional summary for equity research use
