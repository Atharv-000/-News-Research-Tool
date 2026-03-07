"""
Equity Research News Tool - Streamlit App
Fetches news via NewsAPI and summarizes with LangChain/OpenAI.
This file provides the web UI for deployment on Streamlit Community Cloud.
"""

import streamlit as st
from langchain_config import llm_chain, get_summary


def generate_summary(query: str) -> str:
    """Fetch news and generate an LLM summary with graceful quota fallback."""
    summaries = get_summary(query)
    try:
        return llm_chain.invoke({"query": query, "summaries": summaries})
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower() or "insufficient_quota" in error_msg:
            # Fallback: return raw combined news text if OpenAI quota is exceeded
            return summaries[:3000] + ("..." if len(summaries) > 3000 else "")
        raise


def main():
    st.set_page_config(
        page_title="Equity Research News Tool",
        layout="wide",
    )

    st.title("Equity Research News Tool")
    st.write(
        "Enter an equity/stock/market query below. "
        "The app will fetch recent news via NewsAPI and generate a concise AI summary."
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
                result = generate_summary(query.strip())
            except Exception as e:
                st.error(f"Error while generating summary: {e}")
                return

        st.subheader("Summary")
        st.write(result)


if __name__ == "__main__":
    main()

