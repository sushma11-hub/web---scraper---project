import requests
from bs4 import BeautifulSoup
import json
import time

URL = "https://quotes.toscrape.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (Student Project)"}

quotes_data = []
page_url = URL

while page_url and len(quotes_data) < 100:
    try:
        res = requests.get(page_url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        for quote in soup.select('.quote'):
            text = quote.select_one('.text').get_text(strip=True)
            author = quote.select_one('.author').get_text(strip=True)
            tags = [t.get_text(strip=True) for t in quote.select('.tag')]
            quotes_data.append({"text": text, "author": author, "tags": tags})
            if len(quotes_data) >= 100:
                break
        
        next_btn = soup.select_one('li.next > a')
        page_url = URL + next_btn['href'] if next_btn else None
        time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        break

# Save to files
with open('quotes.json', 'w', encoding='utf-8') as f:
    json.dump(quotes_data, f, indent=2, ensure_ascii=False)

with open('quotes.txt', 'w', encoding='utf-8') as f:
    for q in quotes_data:
        f.write(f"{q['text']} - {q['author']}\n")

print(f"Scraped {len(quotes_data)} quotes")
