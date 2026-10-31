import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.parse import urljoin
import os

load_dotenv()
BASE_URL = os.getenv("BASE_URL", "https://www.cyberathon.com/")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_page_links():

    response = requests.get(
        BASE_URL,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    links = set()

    for a in soup.find_all("a", href=True):

        link = urljoin(BASE_URL, a["href"])

        if link.startswith(BASE_URL):
            links.add(link)

    return links


def scrape_page(url):

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )

    if response.status_code != 200:
        return ""

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # Remove unnecessary content
    for tag in soup([
        "script",
        "style",
        "nav",
        "footer"
    ]):
        tag.decompose()

    text = soup.get_text(
        separator=" ",
        strip=True
    )

    return text


def main():

    os.makedirs(
        "data/scraped_data",
        exist_ok=True
    )

    links = get_page_links()

    print("Total links found:", len(links))

    keywords = [
        "home",
        "about",
        "services",
        "products",
        "internship",
        "careers",
        "blog",
        "gallery",
        "contact"
    ]

    selected_links = []

    for link in links:

        if any(
            keyword in link.lower()
            for keyword in keywords
        ):
            selected_links.append(link)

    # Include homepage
    selected_links.append(BASE_URL)

    selected_links = list(set(selected_links))

    print(
        "Pages selected:",
        len(selected_links)
    )

    for i, url in enumerate(selected_links):

        print(
            f"Scraping {i+1}/{len(selected_links)}:"
        )

        print(url)

        text = scrape_page(url)

        if text:

            filename = (
                f"data/scraped_data/"
                f"page_{i+1}.txt"
            )

            with open(
                filename,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    f"URL: {url}\n\n"
                )

                file.write(text)

    print("Scraping completed!")


if __name__ == "__main__":
    main()