from scrapy import scraping_top_url
from bs4 import BeautifulSoup
import requests
import time
import csv
import pandas as pd
from requests.exceptions import RequestException

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
    # return 0  # Return 0 or an appropriate default value if the div is not found

reviewlist= []
def extractReviews(response_content):
    global reviewlist
    soup = BeautifulSoup(response_content, "html.parser")
    reviews = soup.findAll("div", {'data-hook': 'review'})
    # print(reviews)
    for items in reviews:
        try:
            review = {
                'Review Title': items.find('a', {'data-hook': 'review-title'}).get_text().split("stars")[1].strip(),
                'Rating': items.find('i', {'data-hook': 'review-star-rating'}).get_text(),
                'Review Body': items.find('span', {'data-hook': 'review-body'}).get_text()
            }
            reviewlist.append(review)
        except Exception as e:
            print(e)
            

href = []
def url_sessions(urls, headers):
    with requests.Session() as session:
        session.headers.update(headers)
        for url in urls:
            if url == 0:
                continue
            modified_url = f"{url}&pageNumber={1}&sortBy=recent"
            response = session.get(modified_url)
            if response.ok:
                pgNumber = page(response.content)
                for i in range(pgNumber):
                    modified_Pgurl = f"{url}&pageNumber={1 + i}&sortBy=recent"
                    response_content = session.get(modified_Pgurl)
                    if response_content.ok:
                        href.append(modified_Pgurl)

def idk(href, headers):
    with requests.Session() as session:
        session.headers.update(headers)
        for url in href:
            if url == 0:
                continue
            max_tries = 21
            attempts = 0
            response = None
            while attempts < max_tries:
                try:
                    response = session.get(url)
                    if response.ok:
                        print(f"Successfully fetched data from {url}")
                        extractReviews(response.content)
                        break
                except RequestException as e:
                    print(f"An error occurred: {e}")
                attempts += 1
                if attempts < max_tries:
                    session.headers.update(headers)
                    time.sleep(1)
                    

def main(user_input):

    imageUrl, Stars, fiveStarReviewUrl, fourStarReviewUrl, threeStarReviewUrl, twoStarReviewUrl, oneStarReviewUrl = scraping_top_url(user_input)

    if fiveStarReviewUrl != 0:
        fiveStarReviewUrl = fiveStarReviewUrl.replace("#reviews-filter-bar", "").replace("five_star", "all_stars").replace("ref=acr_dp_hist_5", "ref=cm_cr_arp_d_viewopt_sr")
    else:
        fiveStarReviewUrl = 0

    if fourStarReviewUrl != 0:
        fourStarReviewUrl = fourStarReviewUrl.replace("#reviews-filter-bar", "")
    else:
        fourStarReviewUrl = 0

    if threeStarReviewUrl != 0:
        threeStarReviewUrl = threeStarReviewUrl.replace("#reviews-filter-bar", "")
    else:
        threeStarReviewUrl = 0

    if twoStarReviewUrl != 0:
        twoStarReviewUrl = twoStarReviewUrl.replace("#reviews-filter-bar", "")
    else:
        twoStarReviewUrl = 0

    if oneStarReviewUrl != 0:
        oneStarReviewUrl= oneStarReviewUrl.replace("#reviews-filter-bar", "")
    else:
        oneStarReviewUrl = 0

    headers = {
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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
        "X-Amzn-Trace-Id": "Root=1-667c53fe-22aa4a273644bb2924a2fea4"
    }

    urls = [fiveStarReviewUrl]

    url_sessions(urls, headers)
    idk(href, headers)
    print(len(reviewlist))
    df = pd.DataFrame(reviewlist)
    df.to_csv("reviews.csv", index=False)
    df.to_json("dummy.json", index=False)
    return reviewlist, imageUrl, Stars

if __name__ == "__main__":
    x = input("Product: ")
    main(x)
