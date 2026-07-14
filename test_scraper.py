import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, urlunsplit


url = "https://www.ynet.co.il"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
response.raise_for_status()

html = response.text

soup = BeautifulSoup(html, "html.parser")


articles = []
seen_urls = set()

bad_titles = [
    "צור קשר",
    "מדיניות פרטיות",
    "תנאי שימוש",
    "הרשמה",
    "כניסה"
]


for a in soup.find_all("a", href=True):

    href = a["href"]

    # Only keep news article links
    if "/news/article/" in href:

        # Clean URL and remove fragments like #autoplay
        parts = urlsplit(href)

        if parts.scheme == "":
            cleaned_url = "https://www.ynet.co.il" + parts.path
        else:
            cleaned_url = urlunsplit(
                (
                    parts.scheme,
                    parts.netloc,
                    parts.path,
                    parts.query,
                    ""
                )
            )

        title = a.get_text(" ", strip=True)

        # Keep only real-looking headlines
        if (
            title
            and len(title) < 150
            and not any(bad in title for bad in bad_titles)
            and cleaned_url not in seen_urls
        ):

            seen_urls.add(cleaned_url)

            articles.append(
                {
                    "title": title,
                    "url": cleaned_url
                }
            )


print("Found", len(articles), "headlines\n")


for article in articles[:30]:
    print(article["title"])
    print(article["url"])
    print("---")


# Save articles as JSON
with open("ynet_articles.json", "w", encoding="utf-8") as f:
    json.dump(
        articles,
        f,
        ensure_ascii=False,
        indent=2
    )


print("\nSaved to ynet_articles.json")