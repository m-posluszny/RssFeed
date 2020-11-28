import rsshandler

def main():
    h = rsshandler.RSSHandler()

    url = 'https://xkcd.com/rss.xml'
    h.retriveDataFromURL(url)

if __name__ == "__main__":
    main()
