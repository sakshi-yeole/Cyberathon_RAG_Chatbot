import requests
from bs4 import BeautifulSoup

# -----------------------------------------
# 1. Single webpage URL
# -----------------------------------------
url = "https://www.cyberathon.com/seo-marketing"

# -----------------------------------------
# 2. Output TXT file
# -----------------------------------------
output_file = "scraped_data.txt"

# -----------------------------------------
# 3. Get webpage
# -----------------------------------------
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(
    url,
    headers=headers,
    timeout=10
)

response.raise_for_status()

# -----------------------------------------
# 4. Parse webpage
# -----------------------------------------
soup = BeautifulSoup(response.text, "html.parser")

# Remove unnecessary content
for tag in soup(["script", "style", "nav", "footer", "header"]):
    tag.decompose()

# Get webpage text
text = soup.get_text(
    separator="\n",
    strip=True
)

# -----------------------------------------
# 5. Save data into TXT file
# -----------------------------------------
with open(output_file, "w", encoding="utf-8") as file:
    file.write("SCRAPED WEBPAGE DATA\n")
    file.write("=" * 50 + "\n\n")

    file.write(f"URL: {url}\n\n")

    file.write(text)

print("Scraping completed successfully!")
print(f"TXT file created: {output_file}")