import wikipediaapi
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class CustomWikipediaAPI(wikipediaapi.Wikipedia):
    def __init__(self, lang='en', user_agent=None):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': user_agent})
        
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[ 500, 502, 503, 504 ])
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount('https://', adapter)
        self.session.mount('http://', adapter)
        
        super().__init__(lang)
        self._wiki = self.session

def get_random_wikipedia_article():
    user_agent = "MyWikipediaBot/1.0 (https://github.com/yourusername/yourrepo; your_email@example.com)"
    wiki_wiki = CustomWikipediaAPI('en', user_agent=user_agent)
    
    # Fetch a random Wikipedia article URL
    response = requests.get("https://en.wikipedia.org/wiki/Special:Random", headers={'User-Agent': user_agent})
    
    if response.status_code == 200:
        # The response URL is the URL of the random article
        random_article_url = response.url
        # Extract the title of the article from the URL
        random_article_title = random_article_url.split('/')[-1]
        
        # Fetch the article
        page = wiki_wiki.page(random_article_title)
        
        if page.exists():
            print(f"Title: {page.title}")
            print(f"Summary: {page.summary[:500]}...")  # Print first 500 characters of the summary
        else:
            print("The article does not exist.")
    else:
        print("Failed to fetch a random article.")

# Get a random Wikipedia article
get_random_wikipedia_article()


