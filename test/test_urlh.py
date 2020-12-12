import unittest
from libs.urlhandler import URLHandler
from libs.databasehandler import DatabaseHandler

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

    def test_basic_operations(self):
        from libs.credhandler import CredentialsHandler

        db = DatabaseHandler(db_path = "pytests/", dbIsTemp = True)
        cdh = CredentialsHandler('unittest', 'unittestpassword')
        cdh.encryptCredentials()

        self.assertEqual(cdh.doesUserExist(), False)
        cdh.createUser()
        self.assertEqual(cdh.doesUserExist(), True)

        url = 'https://feeds.simplecast.com/6HzeyO6b'
        urlh = URLHandler()

        res = db.getEntry('unittest')
        self.assertNotEqual(len(res['urls']), 0)
        self.assertEqual(len([l for l in res['urls'] if l['actual_url'] == url]), 0)

        URLHandler.addURL(url)
        
        res = db.getEntry('unittest')
        self.assertNotEqual(len(res['urls']), 0)
        self.assertEqual(len([l for l in res['urls'] if l['actual_url'] == url]), 1)
        
        DatabaseHandler.destroyDatabase()

    def test_basic_operations_with_fetching(self):
        from libs.credhandler import CredentialsHandler
        from libs.rsshandler import RSSHandler

        db = DatabaseHandler(db_path = "pytests/", dbIsTemp = True)
        cdh = CredentialsHandler('unittest', 'unittestpassword')
        cdh.encryptCredentials()

        cdh.createUser()

        url = 'https://feeds.simplecast.com/6HzeyO6b'
        URLHandler.addURL(url)
        
        res = db.getEntry('unittest')
        self.assertNotEqual(len(res['urls']), 0)
        self.assertEqual(len([l for l in res['urls'] if l['actual_url'] == url]), 1)

        urlentry = next(filter(lambda x: x['actual_url'] == url, res['urls']))
        self.assertEqual(len(urlentry['articles']), 0)

        rssh = RSSHandler()
        rssh.retriveDataFromURL(url)
        self.assertEqual(rssh.fetchIsSuccess(), True)

        rssh.parseXML()
        art = rssh.returnArticles()

        self.assertNotEqual(len(art), 0)

        URLHandler.appendDownloadedArticles(url, art)

        res = db.getEntry('unittest')
        urlentry = next(filter(lambda x: x['actual_url'] == url, res['urls']))
        self.assertNotEqual(len(urlentry['articles']), 0)

        DatabaseHandler.destroyDatabase()
