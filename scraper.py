import requests
import json
import os, os.path
import errno

URL_DOMAIN = "https://31minutos.fandom.com"
ARTICLE_ENDPOINT = "/api.php?action=parse&pageid={}&prop=wikitext&format=json&utf8=1"

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')

class Article():
    def __init__(self, id):
        self.id = id
        self._title = None
        self._wikitext = None

    def retrieve(self):
        response = requests.get(
            url=URL_DOMAIN+ARTICLE_ENDPOINT.format(self.id)
        ).json()
        return response
    
    def fill(self):
        response = self.retrieve()
        self._title = response["parse"]["title"]
        self._wikitext = response["parse"]["wikitext"]["*"]
    
    @property
    def title(self):
        if self._title is None:
            self.fill()
        return self._title

    @property
    def wikitext(self):
        if self._wikitext is None:
            self.fill()
        return self._wikitext

    def write(self,folder="Articles"):
        filename = os.path.join(folder, self.title+".txt")
        with safe_open_w(filename) as file:
            file.write(self.wikitext)

def get_articles(limit=1000):
    response = requests.get(
        url=URL_DOMAIN+"/api/v1/Articles/List?limit={}".format(limit)
    ).json()
    return response
    
def download_articles():
    articles = get_articles()["items"]
    for article in articles:
        article_id = article["id"]
        article_title = article["title"]
        print("Writing article {} with id {}".format(article_title, article_id))
        new_article = Article(article_id)
        new_article.write()
        
