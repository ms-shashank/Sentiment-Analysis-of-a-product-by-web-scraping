# import requests
# from bs4 import BeautifulSoup
# import random

# def top_product_url(product_name):

#     # product_name = 'PS5 console'
#     url = f'https://www.amazon.in/s?k={product_name.replace(" ", "+")}'
    
#     userAgents = [
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0',
#         'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
#         'Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0'
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
#         'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
#         'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
#         'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'
#         ]

#     headers = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", 
#     "Accept-Encoding": "gzip, deflate, br, zstd", 
#     "Accept-Language": "en-US,en;q=0.5", 
#     "Priority": "u=1", 
#     "Sec-Fetch-Dest": "document", 
#     "Sec-Fetch-Mode": "navigate", 
#     "Sec-Fetch-Site": "cross-site", 
#     "Sec-Fetch-User": "?1", 
#     "Sec-Gpc": "1", 
#     "Upgrade-Insecure-Requests": "1", 
#     "User-Agent": random.choice(userAgents), 
#     "X-Amzn-Trace-Id": "Root=1-667c53fe-22aa4a273644bb2924a2fea4"
#   }

#     while True:
#         for i in userAgents:
#             response = requests.get(url, headers)
#             if response.status_code == 200:
#                 break
#         if response.ok:
#             break
#         else:
#             continue
            
#         #response = requests.get(url, headers={'User-Agent': random.choice(userAgents)})
    
#     # print(response.status_code)
#     # print(response.request.headers)
    
    
#     if response.ok:
#         # Create a BeautifulSoup object and specify the parser
#         soup = BeautifulSoup(response.text, 'html.parser')
    
#         # to find the <a> tag from the html since the class and href to that is in the <a> and we need that class so we will extract from this method
#         product_link = soup.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    
#         if product_link:
#             top_product_url = 'https://www.amazon.in' + product_link['href']
#             #print(f"Top Product URL: {top_product_url}")
#             return top_product_url
#         else:
#             print("No product found in search results.")
#     else:
#         print('Failed to retrieve the webpage')

# if __name__ == "__main__":
#     print(top_product_url("iphone 15 pro max"))


import requests
from bs4 import BeautifulSoup
import random

def top_product_url(product_name):
    url = f'https://www.amazon.in/s?k={product_name.replace(" ", "+")}'

    userAgents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0'
    ]

    headers_template = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", 
        "Accept-Encoding": "gzip, deflate, br, zstd", 
        "Accept-Language": "en-US,en;q=0.5", 
        "Priority": "u=1", 
        "Sec-Fetch-Dest": "document", 
        "Sec-Fetch-Mode": "navigate", 
        "Sec-Fetch-Site": "cross-site", 
        "Sec-Fetch-User": "?1", 
        "Sec-Gpc": "1", 
        "Upgrade-Insecure-Requests": "1", 
        "X-Amzn-Trace-Id": "Root=1-667c53fe-22aa4a273644bb2924a2fea4"
    }

    retries = 5
    for _ in range(retries):
        headers = headers_template.copy()
        headers["User-Agent"] = random.choice(userAgents)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            product_link = soup.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
            if product_link:
                top_product_url = 'https://www.amazon.in' + product_link['href']
                return top_product_url
            else:
                print("No product found in search results.")
                return None
        else:
            print(f"Attempt {_ + 1} failed with status code {response.status_code}")

    print('Failed to retrieve the webpage after several attempts')
    return None

if __name__ == "__main__":
    print(top_product_url("iphone 15 pro max"))
