import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, urlunsplit


# Ynet categories to scrape
urls = [
    "https://www.ynet.co.il/news/category/4502",
    "https://www.ynet.co.il/news/category/192"
]


headers = {
    "User-Agent": "Mozilla/5.0"
}


articles = []
seen_urls = set()


bad_titles = [
    "צור קשר",
    "מדיניות פרטיות",
    "תנאי שימוש",
    "הרשמה",
    "כניסה"
]


for url in urls:

    print("Checking:", url)

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")


    for a in soup.find_all("a", href=True):

        href = a["href"]

        # Only article links
        if "/news/article/" not in href:
            continue


        # Clean URL
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


        # Filter bad titles
        if (
            not title
            or len(title) > 150
            or any(bad in title for bad in bad_titles)
            or cleaned_url in seen_urls
        ):
            continue


        seen_urls.add(cleaned_url)


        # Get article summary
        description = ""

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


            meta = article_soup.find(
                "meta",
                attrs={"name": "description"}
            )


            if meta:
                description = meta.get("content", "")


        except Exception as e:
            print("Could not get summary:", title, e)


        articles.append(
            {
                "title": title,
                "url": cleaned_url,
                "description": description
            }
        )

        print("Added:", title)



print()
print("Found", len(articles), "articles")


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