"""
Equity Research News Tool - Streamlit App
Fetches news via NewsAPI and summarizes with LangChain/OpenAI.
This file provides the web UI for deployment on Streamlit Community Cloud.
"""

import streamlit as st
from langchain_config import llm_chain, get_articles_and_summary


def generate_summary_and_articles(query: str):
    """
    Fetch news articles and generate an LLM summary with graceful quota fallback.
    Returns (summary_text, articles_list).
    """
    articles, summaries = get_articles_and_summary(query)
    try:
        summary = llm_chain.invoke({"query": query, "summaries": summaries})
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower() or "insufficient_quota" in error_msg:
            # Fallback: return raw combined news text if OpenAI quota is exceeded
            summary = summaries[:3000] + ("..." if len(summaries) > 3000 else "")
        else:
            raise
    return summary, articles


def main():
    st.set_page_config(
        page_title="Equity Research News Tool",
        layout="wide",
    )

    st.title("Equity Research News Tool")
    st.write(
        "Enter an equity/stock/market query below. "
        "The app will fetch recent news via NewsAPI, generate a concise AI summary, "
        "and show links to the underlying articles."
    )

    query = st.text_input(
        "Query",
        placeholder="e.g. Tesla stock, NIFTY 50, Federal Reserve, crude oil prices",
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        run = st.button("Summarize")

    if run:
        if not query.strip():
            st.warning("Please enter a query before running the summary.")
            return

        with st.spinner("Fetching news and generating summary..."):
            try:
                summary, articles = generate_summary_and_articles(query.strip())
            except Exception as e:
                st.error(f"Error while generating summary: {e}")
                return

        st.subheader("Summary")
        st.write(summary)

        if articles:
            st.subheader("Source articles")
            for article in articles:
                title = article.get("title") or "Untitled article"
                url = article.get("url")
                source = (article.get("source") or {}).get("name") if isinstance(article.get("source"), dict) else None
                published = article.get("publishedAt")

                meta_parts = [p for p in [source, published] if p]
                meta = " • ".join(meta_parts)

                if url:
                    st.markdown(f"- [{title}]({url})")
                else:
                    st.markdown(f"- {title}")

                if meta:
                    st.markdown(f"  \n  _{meta}_")


if __name__ == "__main__":
    main()

