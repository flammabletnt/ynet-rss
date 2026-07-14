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

soup = BeautifulSoup(response.text, "html.parser")

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

    if "/news/article/" not in href:
        continue

    parts = urlsplit(href)

    if parts.scheme == "":
        cleaned_url = "https://www.ynet.co.il" + parts.path
    else:
        cleaned_url = urlunsplit(
            (parts.scheme, parts.netloc, parts.path, parts.query, "")
        )

    title = a.get_text(" ", strip=True)

    if (
        title
        and len(title) < 150
        and not any(bad in title for bad in bad_titles)
        and cleaned_url not in seen_urls
    ):

        seen_urls.add(cleaned_url)

        # Get article page
        try:
            article_response = requests.get(
                cleaned_url,
                headers=headers,
                timeout=10
            )

            article_soup = BeautifulSoup(
                article_response.text,
                "html.parser"
            )

            description = ""

            # Look for meta description
            meta = article_soup.find(
                "meta",
                attrs={"name": "description"}
            )

            if meta:
                description = meta.get("content", "")

            articles.append({
                "title": title,
                "url": cleaned_url,
                "description": description
            })

            print("Added:", title)

        except Exception as e:
            print("Failed:", title, e)


print("\nFound", len(articles), "articles")


with open(
    "ynet_articles.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        articles,
        f,
        ensure_ascii=False,
        indent=2
    )

print("Saved ynet_articles.json")