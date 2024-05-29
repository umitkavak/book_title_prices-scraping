# Import Libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Fetch HTML Content
def fetch_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    return response.text
    
# Parse HTML Content
def parse_html(html_content):
    return BeautifulSoup(html_content, 'html.parser')
    
# Extract data
def extract_books(soup):
    books = []
    book_elements = soup.find_all('article', class_='product_pod')
    
    for book in book_elements:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').get_text()
        books.append({'title': title, 'price': price})
    
    return books
    
# Save data to CSV file
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    

def main():
    base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
    all_books = []
    
    for page_num in range(1, 50):  # Assuming there are 50 pages
        url = base_url.format(page_num)
        html_content = fetch_html(url)
        soup = parse_html(html_content)
        books = extract_books(soup)
        all_books.extend(books)
        print(f'Scraped page number is {page_num}')
    
    save_to_csv(all_books, 'Allbooks.csv')
    print(f'Scraped {len(all_books)} books and saved to books.csv')
        


if __name__ == '__main__':
        main()

