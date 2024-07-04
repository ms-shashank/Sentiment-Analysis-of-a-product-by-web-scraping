from scrapy import scraping_top_url
from bs4 import BeautifulSoup
import requests
import time
import csv
import pandas as pd
from requests.exceptions import RequestException

# reviewlist = []

def extract_reviews(response_content, reviewlist):
    soup = BeautifulSoup(response_content, "html.parser")
    reviews = soup.findAll("div", {"data-hook": "review"})
    for items in reviews:
        try:
            review = {
                'Review Title': items.find('a', {'data-hook': 'review-title'}).get_text().split("stars")[1].strip(),
                'Rating': items.find('i', {'data-hook': 'review-star-rating'}).get_text(),
                'Review Body': items.find('span', class_ = "a-size-base review-text review-text-content").get_text()
            }
            reviewlist.append(review)
        except Exception as e:
            print(e)

def url_sessions(urls, userAgents, reviewlist):
 
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

    with requests.Session() as session:
        session.headers.update(headers)
        for url in urls:
            if url == 0:
                continue
            pg = 1
            while True:
                modified_url = f"{url}&pageNumber={pg}&sortBy=recent"
                max_tries = 21
                attempts = 0
                response = None
                while attempts < max_tries and not response:
                    try:
                        response = session.get(modified_url)
                        if response.status_code == 200:
                            print(f"Successfully fetched data from {modified_url}")
                            extract_reviews(response.content, reviewlist)
                            soup = BeautifulSoup(response.content, "html.parser")
                            next_page = soup.find('li', class_= 'a-last')
                            if next_page and 'a-disabled a-last' not in next_page['class']:
                                pg += 1
                            else:
                                raise StopIteration
                        break
                    except RequestException as e:
                        print(f"An error occurred: {e}")
                    except StopIteration:
                        break
                    finally:
                        if attempts < max_tries - 1:
                            session.headers.update({'User-Agent': userAgents[attempts % len(userAgents)]})
                        time.sleep(3)
                    attempts += 1
                try:
                    if response is None or 'a-disabled a-last' in next_page.get('class', []):
                        break
                except AttributeError:
                    break

def main(user_input, session_id):
    imageUrl, Stars, fiveStarReviewUrl, fourStarReviewUrl, threeStarReviewUrl, twoStarReviewUrl, oneStarReviewUrl = scraping_top_url(user_input, session_id)
    reviewlist = []
    urls = []
    if fiveStarReviewUrl:
        fiveStarReviewUrl = fiveStarReviewUrl.replace("#reviews-filter-bar", "")
        urls.append(fiveStarReviewUrl)
    if fourStarReviewUrl:
        fourStarReviewUrl = fourStarReviewUrl.replace("#reviews-filter-bar", "")
        urls.append(fourStarReviewUrl)
    if threeStarReviewUrl:
        threeStarReviewUrl = threeStarReviewUrl.replace("#reviews-filter-bar", "")
        urls.append(threeStarReviewUrl)
    if twoStarReviewUrl:
        twoStarReviewUrl = twoStarReviewUrl.replace("#reviews-filter-bar", "")
        urls.append(twoStarReviewUrl)
    if oneStarReviewUrl:
        oneStarReviewUrl = oneStarReviewUrl.replace("#reviews-filter-bar", "")
        urls.append(oneStarReviewUrl)

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

    url_sessions(urls, userAgents, reviewlist)
    df = pd.DataFrame(reviewlist)
    # df.to_json(f"reviews_{session_id}.json", index=False)
    df.to_csv(f"reviews_{session_id}.csv", index=False)
    reviewlist.clear()
    return reviewlist, imageUrl, Stars

if __name__ == "__main__":
    x = input("Product: ")
    session_id = input("Session ID: ")
    main(x, session_id)
    