import requests
from bs4 import BeautifulSoup
import feedparser

def current_price():
    endpoint = "https://api.coingecko.com/api/v3/simple/price"
    cryptocurrencies = ["bitcoin", "ethereum", "solana"]
    response = requests.get(endpoint, params={"ids": ",".join(cryptocurrencies), "vs_currencies": "usd"})
    prices = response.json()
    print("Bitcoin: ${0:.2f}".format(prices["bitcoin"]["usd"]))
    print("Ethereum: ${0:.2f}".format(prices["ethereum"]["usd"]))
    print("Solana: ${0:.2f}".format(prices["solana"]["usd"]))

def crypto_rss():
    feed_url = "https://Blockchain.News/RSS/"
    feed = feedparser.parse(feed_url)
    news_articles = [] 
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        news_articles.append({
            'Title': title,
            'Link': link
        })
    for article in news_articles:
        print(article)

def crypto_updater():
    current_price()
    crypto_rss()

crypto_updater()
