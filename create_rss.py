import json
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator


# Load scraped articles
with open("ynet_articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)


# Create RSS feed
fg = FeedGenerator()

fg.id("https://www.ynet.co.il")
fg.title("Ynet News - Custom RSS")
fg.link(
    href="https://www.ynet.co.il",
    rel="alternate"
)
fg.description("Custom RSS feed created from Ynet headlines")
fg.language("he")


# Add articles
for article in articles:

    entry = fg.add_entry()

    entry.id(article["url"])
    entry.title(article["title"])
    entry.link(href=article["url"])

    # RSS requires timezone-aware datetime
    entry.pubDate(datetime.now(timezone.utc))

    entry.description(
     f'<a href="{article["url"]}">Read article on Ynet</a>'
    )


# Save RSS file
fg.rss_file("ynet_rss.xml", pretty=True)


print("Created ynet_rss.xml")