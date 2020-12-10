import unittest
from libs.urlhandler import URLHandler

class TestURLHandler(unittest.TestCase):

    def test_correct_url(self):
        urlh = URLHandler()

        self.assertEqual(urlh.stringIsURL('https://xkcd.com/rss.xml'), True)
        self.assertEqual(urlh.stringIsURL('https://podcastfeeds.nbcnews.com/dateline-nbc'), True)
        self.assertEqual(urlh.stringIsURL('https://mcsorleys.barstoolsports.com/feed/call-her-daddy'), True)
        self.assertEqual(urlh.stringIsURL('https://feeds.megaphone.fm/WWO8086402096'), True)
        self.assertEqual(urlh.stringIsURL('http://rss.art19.com/the-daily'), True)
        self.assertEqual(urlh.stringIsURL('https://feeds.megaphone.fm/unlocking-us'), True)
        self.assertEqual(urlh.stringIsURL('https://feeds.megaphone.fm/ADL9840290619'), True)
        self.assertEqual(urlh.stringIsURL('https://feeds.npr.org/510312/podcast.xml'), True)
        self.assertEqual(urlh.stringIsURL('https://feeds.simplecast.com/6HzeyO6b'), True)
        self.assertEqual(urlh.stringIsURL('http://joeroganexp.joerogan.libsynpro.com/rss'), True)

    def test_incorrect_url(self):
        urlh = URLHandler()

        self.assertEqual(urlh.stringIsURL('hps://xkcd.com/rss.xml'), False)
        self.assertEqual(urlh.stringIsURL('ttps://podcastfeeds.nbcnews.com/dateline-nbc'), False)
        self.assertEqual(urlh.stringIsURL('https://.barstoolsports.com/feed/call-her-daddy'), False)
        self.assertEqual(urlh.stringIsURL('//feeds.megaphone.fm/WWO8086402096'), False)
        self.assertEqual(urlh.stringIsURL('rss.art19.com/the-daily'), False)
        self.assertEqual(urlh.stringIsURL(':feeds.megaphone.fm/unlocking-us'), False)
        self.assertEqual(urlh.stringIsURL('ht/feeds.megaphone.fm/ADL9840290619'), False)
        self.assertEqual(urlh.stringIsURL('https:\\feedsnpro/////rg510313podcas'), False)
