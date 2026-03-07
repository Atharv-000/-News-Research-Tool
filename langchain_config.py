# langchain_config.py

import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from langchain_openai import OpenAI                          # ← modern import (legacy completions)
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from newsapi import NewsApiClient


openai_api_key = os.getenv("OPENAI_API_KEY")
newsapi_key    = os.getenv("NEWSAPI_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set!")
if not newsapi_key:
    raise ValueError("NEWSAPI_KEY environment variable not set!")


llm = OpenAI(
    api_key=openai_api_key,
    model="gpt-3.5-turbo-instruct",          # or "text-davinci-003" if still available
    temperature=0.3,
    max_tokens=1500
)

# ── Phase 4: NewsAPI integration ─────────────────────────────────────────────
newsapi = NewsApiClient(api_key=newsapi_key)

def get_news_articles(query):
    articles = newsapi.get_everything(
        q=query,
        language='en',
        sort_by='relevancy',
        page_size=10                      # keep small to avoid token limits
    )
    return articles['articles']

def summarize_articles(articles):
    summaries = []
    for article in articles:
        desc = article.get('description') or article.get('title') or ""
        if desc:
            summaries.append(desc)
    return " ".join(summaries) if summaries else "No descriptions found."

def get_articles_and_summary(query):
    articles = get_news_articles(query)
    combined_text = summarize_articles(articles)
    return articles, combined_text

def get_summary(query):
    _, combined_text = get_articles_and_summary(query)
    return combined_text

# ── Prompt & Chain (updated to handle summaries) ──────────────────────────────
template = """
You are an AI assistant helping an equity research analyst.
Given the following user query and the extracted news article texts/summaries below,
provide a concise, professional overall summary of the most relevant recent news.

Query: {query}

Article texts / summaries:
{summaries}

Summary:
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["query", "summaries"]
)

llm_chain = prompt | llm | StrOutputParser()


if __name__ == "__main__":
    import sys
    query = "equity market trends"
    combined_text = get_summary(query)
    try:
        result = llm_chain.invoke({"query": query, "summaries": combined_text})
        print(result)
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower() or "insufficient_quota" in error_msg:
            print("OpenAI API quota exceeded (429). Add billing at https://platform.openai.com/account/billing", file=sys.stderr)
            print("\n--- News summary (without LLM) ---\n", file=sys.stderr)
        else:
            print(f"Error: {e}", file=sys.stderr)
        # Fallback: print raw news summary
        print(combined_text[:2000] + ("..." if len(combined_text) > 2000 else ""))
        sys.exit(1)