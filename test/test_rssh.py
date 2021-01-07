import unittest
from libs.rsshandler import RSSHandler


class TestURLHandler(unittest.TestCase):

    def test_correct_usage(self):
        rssh = RSSHandler()

        rssh.fetch_from_url('https://xkcd.com/rss.xml')
        self.assertEqual(rssh.fetch_is_success(), True)

        rssh.parse_xml()
        self.assertNotEqual(len(rssh.return_articles()), 0)

    def test_incorrect_usage(self):
        rssh = RSSHandler()

        self.assertEqual(rssh.fetch_is_success(), False)

    def test_correct_article_print(self):
        rssh = RSSHandler()

        rssh.fetch_from_url('https://xkcd.com/rss.xml')
        self.assertEqual(rssh.fetch_is_success(), True)

        rssh.parse_xml()

        a = rssh.return_articles()
        self.assertNotEqual(len(a), 0)

        s = '{}'.format(a[0])
        self.assertNotEqual(len(s), 0)
