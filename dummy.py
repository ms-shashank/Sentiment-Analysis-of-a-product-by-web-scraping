from scrapy import scraping_rating_and_reviews, scraping_top_url
from bs4 import BeautifulSoup
import requests
import time
import csv
import pandas as pd
from requests.exceptions import RequestException

Stars, fiveStarReviewUrl, fourStarReviewUrl, threeStarReviewUrl, twoStarReviewUrl, oneStarReviewUrl = scraping_top_url()

if fiveStarReviewUrl != 0:
    pg = 1
    fiveStarReviewUrl = fiveStarReviewUrl.replace("#reviews-filter-bar", "").replace("five_star", "all_stars").replace("ref=acr_dp_hist_5", "ref=cm_cr_arp_d_viewopt_sr") # f"&pageNumber={pg}" + f"&sortBy=recent"
else:
    fiveStarReviewUrl = 0
    
print(fiveStarReviewUrl)
    
userAgents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'
        ]

def page(response_content):
    soup = BeautifulSoup(response_content, "html.parser")
    reviews_div = soup.find('div', {'data-hook':'cr-filter-info-review-rating-count'})
    if reviews_div:
        reviews_text = reviews_div.get_text().strip()
        print(reviews_text)
        total_reviews = int(reviews_text.split(", ")[1].split(" ")[0])
        return 1 + total_reviews // 10
    else:
        print("The 'cr-filter-info-review-rating-count' div was not found.")
        return 0 
    
reviewlist = []
def extractReviews(modified_url):
    # max_tries = 21
    # attempts = 0
    # response = None
    # while attempts < max_tries and not response:
    #     for i in userAgents:
    #         try:
    #             res = requests.get(modified_url, headers={'User_Agent': i})
    #             if res.status_code == 200:
    #                 # print(i)
    #                 break
    #         except requests.RequestException as e:
    #             print(f"An error occurred: {e}")
    #         time.sleep(0.1)
    #     attempts += 1
    with requests.Session() as sess:
        sess.headers.update({'User-Agent': userAgents[0]})
        res = sess.get(modified_url)
        if res.ok:
            soup = BeautifulSoup(res.content, "html.parser")
            reviews = soup.findAll("div", {'data-hook': 'review'})
            # print(soup)
            # print(reviews)
            for items in reviews:
                try:
                    review = {
                        'Review Title': items.find('a', {'data-hook': 'review-title'}).get_text().split("stars")[1].strip(),
                        'Rating': items.find('i', {'data-hook': 'review-star-rating'}).get_text(),
                        'Review Body': items.find('span', {'data-hook': 'review-body'}).get_text()    
                    }
                    reviewlist.append(review)
                    #puff.append(review)
                except Exception as e:
                    print(e)
            df1 = pd.DataFrame(reviewlist)
            df1.to_json("god.json", index=False)
    
def session(url, userAgents):
    with requests.Session() as session:
        session.headers.update({'User-Agent': userAgents[0]})
        response = session.get(url)
        if response.ok:
            pgNumber = page(response.text)
            for i in range(pgNumber):
                modify_url = f"{url}&pageNumber={i + 1}&sortBy=recent"
                print(modify_url)
                extractReviews(modify_url)
        
        
session(fiveStarReviewUrl, userAgents)