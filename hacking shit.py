import wikipediaapi
import requests

def get_random_wikipedia_article():
    # Define the User-Agent
    user_agent = "MyWikipediaBot/1.0 (https://github.com/yourusername/yourrepo; your_email@example.com)"
    
    # Fetch a random Wikipedia article URL
    response = requests.get("https://en.wikipedia.org/wiki/Special:Random", headers={'User-Agent': user_agent})
    
    if response.status_code == 200:
        # Extract the title from the URL
        random_article_url = response.url
        random_article_title = random_article_url.split('/')[-1]
        
        # Initialize Wikipedia API with User-Agent
        wiki_wiki = wikipediaapi.Wikipedia('en', user_agent=user_agent)
        
        # Fetch the article
        page = wiki_wiki.page(random_article_title)
        
        if page.exists():
            # Print the article title and summary
            print(f"Title: {page.title}")
            print(f"Summary: {page.summary[:500]}...")  # Print first 500 characters of the summary
        else:
            print("The article does not exist.")
    else:
        print("Failed to fetch a random article.")

# Get a random Wikipedia article
get_random_wikipedia_article()





