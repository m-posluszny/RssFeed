import rsshandler

def main():
    h = rsshandler.RSSHandler()

    url = 'https://xkcd.com/rss.xml'
    h.retriveDataFromURL(url)
    h.parseXML()
    articles = h.returnArticles()
    for article in articles:
        print(article)

if __name__ == "__main__":
    main()
