class RSSHandler:
    def __init__(self):
        self.__URL = ''
        self.__websiteContent = ''
        self.__responeCode = ''

    def retriveDataFromURL(self, url):
        import requests

        self.__URL = url

        response = requests.get(url)
        self.__websiteContent = response.text
        self.__responseCode = response.status_code

    def formData(self):
        pass

    def parseXML(self):
        pass

    def returnArticle(self):
        pass
