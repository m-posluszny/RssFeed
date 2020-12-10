import unittest
from libs.rsshandler import RSSHandler

class TestURLHandler(unittest.TestCase):

    def test_correct_usage(self):
        rssh = RSSHandler()

        rssh.retriveDataFromURL('https://xkcd.com/rss.xml')
        self.assertEqual(rssh.fetchIsSuccess(), True)

        rssh.parseXML()
        self.assertNotEqual(len(rssh.returnArticles()), 0)

    def test_incorrect_usage(self):
        rssh = RSSHandler()

        self.assertEqual(rssh.fetchIsSuccess(), False)
