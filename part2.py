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
        # get product name
        asin = soup.find('th', text='ASIN').find_next_sibling('td').text.strip()
        # get product price
        try:
            manufacturer = soup.find('th', text='Manufacturer').find_next_sibling('td').text.strip()
        except AttributeError:
            price = 'NA'
        # get product rating
        try:
           description = soup.find('div', {'id': 'productDescription'}).text.strip()
        except AttributeError:
            rating = 'NA'
        product_data.append([asin,manufacturer,description])
    
    return product_data


def main(url):
    all_product_data = []
    product_data = get_product_data(url)
    print(product_data)
    all_product_data.extend(product_data)
        
    # write data to csv
    with open('product_details.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ASIN', 'Manufacturar','Descripcion'])
        print(all_product_data)
        #writer.writerows(all_product_data)
        
if __name__ == '__main__':
    with open('data.csv', newline='') as csvfile:
     reader = csv.reader(csvfile)
     for row in reader:
        url = row[0]
        #print(url)
        main(url)
