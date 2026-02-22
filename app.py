"""
Equity Research News Tool - CLI Interface
Fetches news via NewsAPI and summarizes with LangChain/OpenAI.
Add your own UI/UX (web, desktop, etc.) by importing from langchain_config.
"""
import argparse
import sys
from langchain_config import llm_chain, get_summary


def run_query(query: str) -> str:
    """Fetch news and generate summary. Returns summary text or None on error."""
    print("Fetching news articles...", file=sys.stderr)
    summaries = get_summary(query)
    print("Generating AI summary...", file=sys.stderr)
    try:
        return llm_chain.invoke({"query": query, "summaries": summaries})
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower() or "insufficient_quota" in error_msg:
            print("OpenAI quota exceeded. Add billing at https://platform.openai.com/account/billing", file=sys.stderr)
            return summaries[:3000] + ("..." if len(summaries) > 3000 else "")
        raise


def main():
    parser = argparse.ArgumentParser(description="Equity Research News Tool - CLI")
    parser.add_argument("query", nargs="?", help="Search query (e.g. 'Tesla stock'). Omit for interactive mode.")
    args = parser.parse_args()

    if args.query:
        print(run_query(args.query))
        return

    # Interactive mode
    print("Equity Research News Tool")
    print("Enter a query to get summarized news. Empty line or Ctrl+C to quit.\n")
    while True:
        try:
            query = input("Query: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break
        if not query:
            break
        result = run_query(query)
        print("\n--- Summary ---\n")
        print(result)
        print("\n")


if __name__ == "__main__":
    main()
