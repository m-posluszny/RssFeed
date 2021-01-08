import unittest
import time
from libs.urlhandler import URLHandler
from libs.databasehandler import DatabaseHandler


class TestURLHandler(unittest.TestCase):

    def test_correct_url(self):
        self.assertEqual(URLHandler.string_is_url(
            'https://xkcd.com/rss.xml'), True)
        self.assertEqual(URLHandler.string_is_url(
            'https://podcastfeeds.nbcnews.com/dateline-nbc'), True)
        self.assertEqual(URLHandler.string_is_url(
            'https://mcsorleys.barstoolsports.com/feed/call-her-daddy'), True)
        self.assertEqual(URLHandler.string_is_url(
            'https://feeds.megaphone.fm/WWO8086402096'), True)
        self.assertEqual(URLHandler.string_is_url(
            'http://rss.art19.com/the-daily'), True)
        self.assertEqual(URLHandler.string_is_url(
            'https://feeds.megaphone.fm/unlocking-us'), True)
        self.assertEqual(URLHandler.string_is_url(
            'https://feeds.megaphone.fm/ADL9840290619'), True)
        self.assertEqual(URLHandler.string_is_url(
            'https://feeds.npr.org/510312/podcast.xml'), True)
        self.assertEqual(URLHandler.string_is_url(
            'https://feeds.simplecast.com/6HzeyO6b'), True)
        self.assertEqual(URLHandler.string_is_url(
            'http://joeroganexp.joerogan.libsynpro.com/rss'), True)

    def test_incorrect_url(self):
        self.assertEqual(URLHandler.string_is_url(
            'hps://xkcd.com/rss.xml'), False)
        self.assertEqual(URLHandler.string_is_url(
            'ttps://podcastfeeds.nbcnews.com/dateline-nbc'), False)
        self.assertEqual(URLHandler.string_is_url(
            '//feeds.megaphone.fm/WWO8086402096'), False)
        self.assertEqual(URLHandler.string_is_url(
            'rss.art19.com/the-daily'), False)
        self.assertEqual(URLHandler.string_is_url(
            ':feeds.megaphone.fm/unlocking-us'), False)
        self.assertEqual(URLHandler.string_is_url(
            'ht/feeds.megaphone.fm/ADL9840290619'), False)
        self.assertEqual(URLHandler.string_is_url(
            'https:\\feedsnpro/////rg510313podcas'), False)

    def test_basic_operations(self):
        from libs.credhandler import CredentialsHandler

        db = DatabaseHandler(db_path="pytests/", dbIsTemp=True)
        cdh = CredentialsHandler('unittest', 'unittestpassword')
        cdh.encrypt_credentials()

        self.assertEqual(cdh.does_user_exist(), False)
        cdh.create_user()
        value = {
            'password': cdh.password,
            'urls': [
                {
                    'actual_url': 'https://xkcd.com/rss.xml',
                    'rss_title': 'xkcd.com',
                    'rss_link': 'https://xkcd.com/',
                    'rss_desc': 'xkcd.com: A webcomic of romance and math humor.',
                    'articles': [
                        {
                                "title": "Wonder Woman 1984",
                                "link": "https://xkcd.com/2396/",
                                "desc": r'<img src="https://imgs.xkcd.com/comics/wonder_woman_1984.png" title="\'Wait, why would you think a movie set in 1984 would do drive-ins as a retro promotion?\' \'You know, 80s stuff. Drive-in movies. Britney Spears doing the hustle. Elvis going on Ed Sullivan and showing off his pog collection.\' \'What year were you born, again?\'" alt="\'Wait, why would you think a movie set in 1984 would do drive-ins as a retro promotion?\' \'You know, 80s stuff. Drive-in movies. Britney Spears doing the hustle. Elvis going on Ed Sullivan and showing off his pog collection.\' \'What year were you born, again?\'" />',
                                "pub_date": "Wed, 09 Dec 2020 05:00:00 -0000",
                                'pub_date_parsed': time.localtime(1607313600),
                                "seen": False,
                        },
                        {
                            'title': 'Covid Precaution Level',
                            'link': 'https://xkcd.com/2395/',
                            'desc': r'<img src="https://imgs.xkcd.com/comics/covid_precaution_level.png" title="It\'s frustrating to calibrate your precautions when there\'s only one kind of really definitive feedback you can get, you can only get it once, and when you do it\'s too late." alt="It\'s frustrating to calibrate your precautions when there\'s only one kind of really definitive feedback you can get, you can only get it once, and when you do it\'s too late." />',
                            'pub_date': 'Mon, 07 Dec 2020 05:00:00 -0000',
                            'pub_date_parsed': time.localtime(1607486400),
                            'seen': True,
                        },
                    ],
                },
            ],
            'groups': {
                'All': [0],
            },
        }
        db.add_entry('unittest',value)
        self.assertEqual(cdh.does_user_exist(), True)

        url = 'https://feeds.simplecast.com/6HzeyO6b'

        res = db.get_entry('unittest')
        self.assertNotEqual(len(res['urls']), 0)
        self.assertEqual(
            len([l for l in res['urls'] if l['actual_url'] == url]), 0)

        URLHandler.add_url(url)

        res = db.get_entry('unittest')
        self.assertNotEqual(len(res['urls']), 0)
        self.assertEqual(
            len([l for l in res['urls'] if l['actual_url'] == url]), 1)

        DatabaseHandler.destroy_database()

    def test_basic_operations_with_fetching(self):
        from libs.credhandler import CredentialsHandler
        from libs.rsshandler import RSSHandler

        db = DatabaseHandler(db_path="pytests/", dbIsTemp=True)
        cdh = CredentialsHandler('unittest', 'unittestpassword')
        cdh.encrypt_credentials()

        cdh.create_user()

        url = 'https://feeds.simplecast.com/6HzeyO6b'
        URLHandler.add_url(url)

        res = db.get_entry('unittest')
        self.assertNotEqual(len(res['urls']), 0)
        self.assertEqual(
            len([l for l in res['urls'] if l['actual_url'] == url]), 1)

        urlentry = next(filter(lambda x: x['actual_url'] == url, res['urls']))
        self.assertEqual(len(urlentry['articles']), 0)

        rssh = RSSHandler()
        rssh.fetch_from_url(url)
        self.assertEqual(rssh.fetch_is_success(), True)

        rssh.parse_xml()
        art = rssh.return_articles()

        self.assertNotEqual(len(art), 0)

        URLHandler.append_downloaded_articles(url, art)

        res = db.get_entry('unittest')
        urlentry = next(filter(lambda x: x['actual_url'] == url, res['urls']))
        self.assertNotEqual(len(urlentry['articles']), 0)

        DatabaseHandler.destroy_database()
