import requests 
import re 

from requests import Session

class GetCatalogue: 
    def __init__(self, url1): 
        self.session = requests.Session()
        self.url1 = url1
        self.found_items = [] 
        self.page_count = 0

        self.compiled_regex_find_items = re.compile('<div data-asin="([a-zA-Z]+([0-9]+[a-zA-Z]+)+)" data-index')
        self.compiled_regex_find_page_count = re.compile('<span class="s-pagination-item s-pagination-disabled" aria-disabled="true">([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?</span>')
    
    def regex_find_items(self, text):
        [self.found_items.append(i[0]) for i in self.compiled_regex_find_items.findall(text)]
        self.found_items = list(set(self.found_items))

    def regex_find_page_count(self, text): 
        self.page_count = int(self.compiled_regex_find_page_count.findall(text)[0][0])

    def get_1(self):
        headers = {
            'authority': 'www.amazon.co.uk',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
            'device-memory': '4',
            'downlink': '9.3',
            'dpr': '0.75',
            'ect': '4g',
            'referer': 'https://www.amazon.co.uk/Beauty-Tools-Accessories/b/',
            'rtt': '150',
            'sec-ch-device-memory': '4',
            'sec-ch-dpr': '0.75',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-ch-viewport-width': '1821',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'viewport-width': '1821',
        }

        response = self.session.get('https://www.amazon.co.uk/b/', headers=headers)
        print(response.text) 
        print(response.headers) 
        print(response.cookies)

    def get_2(self): 
        headers = {
            'authority': 'www.amazon.co.uk',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'device-memory': '4',
            'downlink': '6.55',
            'dpr': '0.75',
            'ect': '4g',
            'rtt': '100',
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

        response = self.session.get(self.url1, headers=headers) 
        self.regex_find_items(response.text) 
        self.regex_find_page_count(response.text) 

        for i in range(self.page_count): 
            i += 1
            response = self.session.get(self.url1+f'&page={i}', headers=headers)
            self.regex_find_items(response.text) 
            print(i)
            print(self.found_items)
        
        return self.found_items 
