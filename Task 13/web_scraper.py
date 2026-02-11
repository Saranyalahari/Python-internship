import requests
from bs4 import BeautifulSoup
import csv

# Website URL (Scrape-Friendly Practice Site)

URL = "http://books.toscrape.com/"

# Fetch HTML Content
def fetch_html(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(" Website fetched successfully\n")
            return response.text
        else:
            print(f"Failed to fetch website. Status Code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(" Error fetching website:", e)
        return None

# Parse and Extract Data

def parse_books(html):
    soup = BeautifulSoup(html, "html.parser")

    books = []

    # Identify book containers
    book_articles = soup.find_all("article", class_="product_pod")

    for book in book_articles:
        try:
            # Extract title
            title = book.h3.a["title"]

            # Extract price
            price = book.find("p", class_="price_color").text

            # Extract rating (stored in class attribute)
            rating = book.find("p", class_="star-rating")["class"][1]

            # Extract link
            link = book.h3.a["href"]

            books.append([title, price, rating, link])

        except (AttributeError, KeyError, TypeError):
            # Handle missing tags safely
            continue

    return books

# Save Data to CSV

def save_to_csv(data):
    with open("books_data.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow(["Title", "Price", "Rating", "Link"])

        # Write rows
        writer.writerows(data)

    print("Data saved to books_data.csv")

# Main Function

def main():
    print("=== Web Scraping Program ===\n")

    html = fetch_html(URL)

    if html:
        books = parse_books(html)

        print(f" {len(books)} books extracted.\n")

        for book in books[:5]:  # Display first 5 books
            print(f"Title  : {book[0]}")
            print(f"Price  : {book[1]}")
            print(f"Rating : {book[2]}")
            print("-" * 40)

        save_to_csv(books)


if __name__ == "__main__":
    main()
