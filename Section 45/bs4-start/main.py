from bs4 import BeautifulSoup
import requests

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return None

def parse_articles(soup):
    articles = soup.find_all(name="span", class_="titleline")
    article_texts = [article.getText() for article in articles]
    article_links = [article.find(name='a').get("href") for article in articles]
    return article_texts, article_links

def parse_upvotes(soup):
    subtexts = soup.findAll(class_="subtext")
    return [int(line.span.span.getText().strip(" points")) if line.span.span else 0 for line in subtexts]

def find_most_upvoted(article_texts, article_links, article_upvotes):
    max_upvotes = max(article_upvotes)
    max_index = article_upvotes.index(max_upvotes)
    return article_texts[max_index], article_links[max_index], max_upvotes

def main():
    url = "https://news.ycombinator.com/"
    yc_web_page = fetch_page(url)
    
    if yc_web_page:
        soup = BeautifulSoup(yc_web_page, 'html.parser')
        article_texts, article_links = parse_articles(soup)
        article_upvotes = parse_upvotes(soup)
        
        most_upvoted_text, most_upvoted_link, most_upvotes = find_most_upvoted(article_texts, article_links, article_upvotes)
        
        print(
            f"Most upvoted article: {most_upvoted_text}\n"
            f"Number of upvotes: {most_upvotes} points\n"
            f"Available at: {most_upvoted_link}."
        )

if __name__ == "__main__":
    main()