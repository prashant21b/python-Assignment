import requests
from bs4 import BeautifulSoup
import csv

def get_product_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    product_data = []
    
    # get product details from each product card
    for card in soup.find_all('div', {'data-component-type': 's-search-result'}):
        # get product URL
        url = 'https://www.amazon.in' + card.find('a', {'class': 'a-link-normal'})['href']
        # get product name
        name = card.find('h2', {'class': 'a-size-mini a-spacing-none a-color-base s-line-clamp-2'}).text.strip()
        # get product price
        try:
            price = card.find('span', {'class': 'a-price-whole'}).text.replace(',', '')
        except AttributeError:
            price = 'NA'
        # get product rating
        try:
            rating = card.find('span', {'class': 'a-icon-alt'}).text.split()[0]
        except AttributeError:
            rating = 'NA'
        # get number of reviews
        try:
            reviews = card.find('span', {'class': 'a-size-base'}).text.replace(',', '').split()[0]
        except AttributeError:
            reviews = 'NA'
        
        product_data.append([url, name, price, rating, reviews])
    
    return product_data


def main():
    all_product_data = []
    
    # scrape data from 20 pages
    for i in range(1, 21):
        url = f'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{i}'
        product_data = get_product_data(url)
        all_product_data.extend(product_data)
        
    # write data to csv
    with open('data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['URL', 'Product Name', 'Price', 'Rating', 'Number of Reviews'])
        writer.writerows(all_product_data)
        
if __name__ == '__main__':
    main()
