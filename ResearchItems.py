import requests 
import re
import json

from requests import Session
from multiprocessing import Pool 
from multiprocessing import Manager 

final_data_list = Manager().list()
def parse_regex(text, id): 
    extraction = {
                'product_title':'',
                'reviews':'',
                'url':'',
                'id': id,  
                'description':'# do you want the description and price? message me on mail, so we can discuss the price.)'
                }

    product_title = re.compile('<span id="productTitle" class="a-size-large product-title-word-break"\>(.*?)\</span>').findall(text)[0]
    extraction['product_title'] = product_title.replace('        ', '').replace('       ', '')
    print(id)

    reviews = re.compile('<span data-hook="top-customer-reviews-title" class="a-size-base"\>(.*?)\</span>').findall(text)
    if 'No customer reviews' in reviews: 
        extraction['reviews'] = None
    else: 
        extraction['reviews'] = re.compile('<span data-hook="rating-out-of-text" class="a-size-medium a-color-base"\>(.*?)\</span>').findall(text)[0][0]

    extraction['url'] = f'https://amazon.co.uk/dp/{id}'

    print(json.dumps(extraction, indent=4))

    return dict(extraction) 
        
def run_scrape(id):
    headers = {
        'authority': 'www.amazon.co.uk',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'device-memory': '4',
        'downlink': '5.85',
        'dpr': '0.75',
        'ect': '4g',
        'rtt': '50',
        'sec-ch-device-memory': '4',
        'sec-ch-dpr': '0.75',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-ch-viewport-width': '1821',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'viewport-width': '1821',
    }

    response = requests.get(f'https://www.amazon.co.uk/dp/{id}', headers=headers)

    final_data_list.append(parse_regex(response.text, id))

def multiprocess_info_parsing(catalogued_items):                                        
    pool = Pool(processes=10)                                               
    pool.map(run_scrape, catalogued_items)
