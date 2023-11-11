from urllib.request import urlopen, Request
from lxml.html import fromstring
from bs4 import BeautifulSoup
import csv

def CsvHeader():
    header = ['Product Title', 'Product Price', 'Product Asin', 'Product URL']
    with open('Amazon_products_data.csv', 'w', encoding='utf-8', newline='') as f:
        csv.writer(f).writerow(header)

def saveCSV(row):
    with open('Amazon_products_data.csv', 'a', encoding='utf-8', newline='') as f:
        csv.writer(f).writerow(row)

def run():
    maxPg = 20
    for pgNo in range(1, maxPg + 1):
        url = f'https://www.amazon.com/s?i=merchant-items&me=A3DQZEP4SGW5UA&page={pgNo}'
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        print(f'Getting: {url}')
        response = urlopen(req).read()
        htmlSoup = fromstring(response, 'lxml')
        products = htmlSoup.xpath('//div//div[contains(@class, "s-title-instructions-style")]')
        print(len(products))
        for indx, product in enumerate(products, start=1):
            prodURL = product.xpath('.//h2/a')[0].get('href')
            prodURL = 'https://www.amazon.com' + prodURL
            if '/dp/' in prodURL:
                prodURL = prodURL.split('ref=')[0]
            prodTitle = product.xpath('.//h2/a/span')[0].text.strip()
            prodAsin = prodURL.split('ref=')[0].split('dp/')[-1].replace('/', '')
            priceTag = product.xpath('//div//a/span[@class="a-price"]/span[contains(@class, "a-offscreen")]')
            price = priceTag[0].text if priceTag else 'None'
            dataRow =  [prodTitle, price, prodAsin, prodURL]
            saveCSV(dataRow)
            item = {
                'Index': indx,
                'Product Title': prodTitle,
                'price': price,
                'Asin': prodAsin,
                'URL': prodURL,
            }
            print(f'[GETTING-INFO] - [PRODUCTS]: {item}')


if __name__ == '__main__':
    CsvHeader()
    run()