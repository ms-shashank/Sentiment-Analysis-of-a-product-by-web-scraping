from prodUrlFetcher import top_product_url
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import random

userAgents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
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

rating = []

def scraping_top_url(user_input, session_id):
    url = top_product_url(user_input)
    img_url, star, fiveStarReview, fourStarReview, threeStarReview, twoStarReview, oneStarReview = scraping_rating_and_reviews(url, session_id)
    return img_url, star, fiveStarReview, fourStarReview, threeStarReview, twoStarReview, oneStarReview      

def scraping_rating_and_reviews(rating_url, session_id):
    retries = 7
    response = None
    image_link = ""
    
    for _ in range(retries):
        headers = headers_template.copy()
        headers["User-Agent"] = random.choice(userAgents)
        response = requests.get(rating_url, headers=headers)
        if response.status_code == 200:
            break

    if response and response.ok:
        soup = BeautifulSoup(response.content, "html.parser")
        try:
            img = soup.find("img", id="landingImage") or \
                soup.find("img", class_="a-dynamic-image a-stretch-horizontal") or \
                soup.find("img", {"data-old-hires": True}) or \
                soup.find("img", src=True)
                
            if img:
                image_link = img["src"]
        except Exception as e:
            print(e)

        star = soup.find_all("td", class_="a-text-right a-nowrap a-nowrap")
        for td in star:
            rating_percentage = td.find_all("a", class_="a-size-base a-link-normal")
            zero_percentage = td.find_all("span", class_="a-size-base")
            for zero in zero_percentage:
                rating.append(zero.get_text())
            for percentage in rating_percentage:
                rating.append(percentage.get_text())

        fiveStarReviewLink = soup.find_all('a', {'class': "a-size-base a-link-normal"})
        fiveStarUrl = fourStarUrl = threeStarUrl = twoStarUrl = oneStarUrl = ""
        if fiveStarReviewLink:
            for hyperlinks in fiveStarReviewLink:
                if 'ref=acr_dp_hist_5?' in hyperlinks['href']:
                    fiveStarUrl = 'https://www.amazon.in' + hyperlinks['href']
                if 'ref=acr_dp_hist_4?' in hyperlinks['href']:
                    fourStarUrl = 'https://www.amazon.in' + hyperlinks['href']
                if 'ref=acr_dp_hist_3?' in hyperlinks['href']:
                    threeStarUrl = 'https://www.amazon.in' + hyperlinks['href']
                if 'ref=acr_dp_hist_2?' in hyperlinks['href']:
                    twoStarUrl = 'https://www.amazon.in' + hyperlinks['href']
                if 'ref=acr_dp_hist_1?' in hyperlinks['href']:
                    oneStarUrl = 'https://www.amazon.in' + hyperlinks['href']

    star_percentages = [float(rates.strip('%')) for rates in rating]
    st = ['5 stars', '4 stars', '3 stars', '2 stars', '1 star']

    with open(f'star_ratings_{session_id}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Star', 'Percentage'])
        for star, percentage in zip(st, star_percentages):
            writer.writerow([star, percentage])

    rating.clear()

    return image_link, rating, fiveStarUrl, fourStarUrl, threeStarUrl, twoStarUrl, oneStarUrl      

if __name__ == "__main__":
    scraping_top_url("iphone 15 pro max", "blah blah")
