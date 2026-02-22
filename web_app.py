from flask import Flask, request, render_template_string
from langchain_config import get_news_articles

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Equity Research News Tool</title>
    <style>
      :root {
        color-scheme: dark;
      }
      * {
        box-sizing: border-box;
      }
      body {
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        max-width: 960px;
        margin: 2rem auto;
        padding: 0 1.5rem 2rem;
        background-color: #0b1015;
        color: #e5e7eb;
      }
      h1 {
        margin-bottom: 0.25rem;
        font-size: 1.9rem;
        color: #f9fafb;
      }
      h2 {
        margin: 1.5rem 0 1rem;
        font-size: 1.3rem;
        color: #e5e7eb;
      }
      p.lead {
        margin: 0 0 1.5rem;
        color: #9ca3af;
      }
      form {
        margin-bottom: 1.75rem;
        padding: 1rem 1.1rem;
        background: radial-gradient(circle at top left, #111827, #020617);
        border-radius: 0.75rem;
        border: 1px solid #1f2937;
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.6);
      }
      label {
        display: block;
        font-size: 0.9rem;
        margin-bottom: 0.35rem;
        color: #9ca3af;
      }
      input[type=text] {
        width: 100%;
        padding: 0.6rem 0.75rem;
        font-size: 0.98rem;
        border-radius: 0.55rem;
        border: 1px solid #374151;
        background-color: #020617;
        color: #e5e7eb;
        outline: none;
        box-shadow: inset 0 0 0 1px rgba(15, 23, 42, 0.6);
      }
      input[type=text]::placeholder {
        color: #6b7280;
      }
      input[type=text]:focus {
        border-color: #38bdf8;
        box-shadow: 0 0 0 1px #38bdf8;
      }
      button {
        margin-top: 0.75rem;
        padding: 0.55rem 1.2rem;
        font-size: 0.95rem;
        border-radius: 999px;
        border: none;
        cursor: pointer;
        background: linear-gradient(135deg, #0ea5e9, #22c55e);
        color: #0b1015;
        font-weight: 600;
        box-shadow: 0 10px 25px rgba(56, 189, 248, 0.35);
      }
      button:hover {
        filter: brightness(1.08);
      }
      button:active {
        transform: translateY(1px);
        box-shadow: 0 6px 18px rgba(56, 189, 248, 0.25);
      }
      .article {
        margin-bottom: 1.2rem;
        padding: 1rem 1.1rem;
        border-radius: 0.75rem;
        border: 1px solid #111827;
        background: radial-gradient(circle at top left, #020617, #020617);
      }
      .article h3 {
        margin: 0 0 0.35rem;
        font-size: 1.05rem;
        color: #f9fafb;
      }
      .article p {
        margin: 0.25rem 0;
        line-height: 1.5;
        color: #d1d5db;
      }
      .source {
        color: #9ca3af;
        font-size: 0.85rem;
      }
      .source span {
        opacity: 0.9;
      }
      a {
        color: #38bdf8;
        text-decoration: none;
        font-weight: 500;
      }
      a:hover {
        text-decoration: underline;
      }
      .error {
        color: #fecaca;
        background-color: rgba(127, 29, 29, 0.4);
        border: 1px solid #b91c1c;
        padding: 0.6rem 0.75rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
      }
      .empty {
        color: #9ca3af;
        font-style: italic;
      }
    </style>
  </head>
  <body>
    <h1>Equity Research News Tool</h1>
    <p class="lead">Dark-themed web view of recent financial news. Enter a topic, company, or macro theme.</p>

    <form method="GET" action="/">
      <label for="q">Search query</label>
      <input id="q" type="text" name="q" placeholder="e.g. Tesla stock, interest rates, emerging markets" value="{{ query or '' }}">
      <button type="submit">Search</button>
    </form>

    {% if error %}
      <div class="error">{{ error }}</div>
    {% endif %}

    {% if articles %}
      <h2>Results for "{{ query }}"</h2>
      {% for a in articles %}
        <div class="article">
          <h3>{{ a.title or 'Untitled article' }}</h3>
          {% if a.description %}
            <p>{{ a.description }}</p>
          {% endif %}
          <p class="source">
            <span>Source: {{ a.source.name if a.source and a.source.name else 'Unknown' }}</span>
            {% if a.publishedAt %}<span> · {{ a.publishedAt }}</span>{% endif %}
          </p>
          {% if a.url %}
            <p><a href="{{ a.url }}" target="_blank" rel="noopener noreferrer">Read full article</a></p>
          {% endif %}
        </div>
      {% endfor %}
    {% elif query %}
      <p class="empty">No articles found for this query.</p>
    {% endif %}
  </body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "").strip()
    articles = []
    error = None
    if query:
        try:
            articles = get_news_articles(query)
        except Exception as e:
            error = f"Error fetching news: {e}"
    return render_template_string(TEMPLATE, query=query, articles=articles, error=error)


if __name__ == "__main__":
    app.run(debug=True)

