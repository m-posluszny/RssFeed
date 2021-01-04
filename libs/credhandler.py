from hashlib import sha1
from libs.databasehandler import DatabaseHandler
import time

class CredentialsHandler:
    lastUsername = ''

    def __init__(self, username, password):

        bytes_passwd = password

        if isinstance(password, str):
            bytes_passwd = password.encode()
        elif not isinstance(password, bytes):
            assert(False)

        self.__username = username
        self.__password = bytes_passwd
        self.__dbHandler = None

        CredentialsHandler.lastUsername = username

    @property
    def password(self):
        return self.__password
    
    @property
    def username(self):
        return self.__username

    def doesUserExist(self):
        dbh = DatabaseHandler()

        result = dbh.getEntry(self.username)

        if result == None:
            return False
        else:
            return True
    
    def createUser(self):
        dbh = DatabaseHandler()

        # NOTE(mateusz): as a testing measure each new user is subscribed to xkcd's rss
        value = { 
                'password': self.password,
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
                    'All': [ 0 ],
                    },
                }

        result = dbh.addEntry(self.username, value)

    def encryptCredentials(self):
        hasher = sha1(self.__password)
        self.__password = hasher.hexdigest()

    def areCredValid(self):
        dbh = DatabaseHandler()

        # Password has to encrypted by this point
        result = dbh.getEntry(self.username)

        if result == None:
            return False
        else:
            if result['password'] == self.password:
                return True
            else:
                return False
