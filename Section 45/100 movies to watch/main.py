import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

def fetch_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")
        return None

def extract_movie_titles(soup):
    return [movie.getText() for movie in soup.find_all(name="h3", class_="title")][::-1]

def save_to_file(movies, filename="movies.txt"):
    with open(filename, mode="w") as file:
        file.write("\n".join(movies))

def main():
    website_html = fetch_website(URL)
    if website_html:
        soup = BeautifulSoup(website_html, "html.parser")
        movies = extract_movie_titles(soup)
        save_to_file(movies)

if __name__ == "__main__":
    main()