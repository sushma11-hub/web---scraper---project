{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Y-A_WBTbEb4v",
        "outputId": "3b1298d0-64d2-4cd1-d8cb-14dbf8d6b1d0"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: requests in /usr/local/lib/python3.13/dist-packages (2.32.4)\n",
            "Requirement already satisfied: beautifulsoup4 in /usr/local/lib/python3.13/dist-packages (4.13.5)\n",
            "Requirement already satisfied: charset_normalizer<4,>=2 in /usr/local/lib/python3.13/dist-packages (from requests) (3.4.9)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.13/dist-packages (from requests) (3.20)\n",
            "Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.13/dist-packages (from requests) (2.5.0)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.13/dist-packages (from requests) (2026.7.22)\n",
            "Requirement already satisfied: soupsieve>1.2 in /usr/local/lib/python3.13/dist-packages (from beautifulsoup4) (3.0.3)\n",
            "Requirement already satisfied: typing-extensions>=4.0.0 in /usr/local/lib/python3.13/dist-packages (from beautifulsoup4) (4.16.0)\n",
            "Total: 100\n"
          ]
        }
      ],
      "source": [
        "!pip install requests beautifulsoup4\n",
        "\n",
        "import json\n",
        "import time\n",
        "import requests\n",
        "from bs4 import BeautifulSoup\n",
        "from collections import Counter\n",
        "\n",
        "BASE = \"https://quotes.toscrape.com\"\n",
        "HEADERS = {\"User-Agent\": \"InternCircle-learning-project (student scraper)\"}\n",
        "\n",
        "def scrape():\n",
        "    url = BASE + \"/\"\n",
        "    quotes = []\n",
        "    while url:\n",
        "        r = requests.get(url, headers=HEADERS, timeout=10)\n",
        "        r.raise_for_status()\n",
        "        soup = BeautifulSoup(r.text, \"html.parser\")\n",
        "        for q in soup.select(\"div.quote\"):\n",
        "            quotes.append({\n",
        "                \"text\": q.select_one(\"span.text\").get_text(strip=True),\n",
        "                \"author\": q.select_one(\"small.author\").get_text(strip=True),\n",
        "                \"tags\": [t.get_text() for t in q.select(\"a.tag\")]\n",
        "            })\n",
        "        nxt = soup.select_one(\"li.next a\")\n",
        "        url = BASE + nxt[\"href\"] if nxt else None\n",
        "        if url:\n",
        "            time.sleep(1)\n",
        "    return quotes\n",
        "\n",
        "def save_and_report(quotes):\n",
        "    with open('quotes.json', 'w', encoding='utf-8') as f:\n",
        "        json.dump(quotes, f, indent=2, ensure_ascii=False)\n",
        "    with open('quotes.txt', 'w', encoding='utf-8') as f:\n",
        "        for i, q in enumerate(quotes, 1):\n",
        "            f.write(f\"{i}. {q['text']} - {q['author']}\\n\")\n",
        "    print(f\"Total: {len(quotes)}\")\n",
        "    with open('README.md', 'w') as f:\n",
        "        f.write(\"# Web Scraper\\nSource: quotes.toscrape.com - safe for scraping, allows robots.txt, slow requests with sleep(1)\")\n",
        "\n",
        "data = scrape()\n",
        "save_and_report(data)"
      ]
    }
  ]
}