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
    df.to_json(f"reviews_{session_id}.json", index=False)
    df.to_csv(f"reviews_{session_id}.csv", index=False)
    reviewlist.clear()
    return reviewlist, imageUrl, Stars

if __name__ == "__main__":
    x = input("Product: ")
    session_id = input("Session ID: ")
    main(x, session_id)
    
    
    
#-------------------------------------By Adding some Different headers the program starts to works-------------------------------------------------------------------------------------
    
# from bs4 import BeautifulSoup
# import requests
# import time
# import csv
# import pandas as pd
# # from selenium import webdriver
# # from webdriver_manager.chrome import ChromeDriverManager
# from requests.exceptions import RequestException

# reviewlist = []
# def extract_reviews(response_content):
#     soup = BeautifulSoup(response_content, "html.parser")
#     reviews = soup.findAll("div", {"data-hook": "review"})
#     # print(soup)
#     # print(reviews)
#     for items in reviews:
#         try:
#             review = {
#                 'Review Title': items.find('a', {'data-hook': 'review-title'}).get_text().split("stars")[1].strip(),
#                 'Rating': items.find('i', {'data-hook': 'review-star-rating'}).get_text(),
#                 #'Review Body': items.find('span', {'data-hook': 'review-body'}).get_text()
#                  'Review Body': items.find('span', class_ = "a-size-base review-text review-text-content").get_text() 
#             }
#             reviewlist.append(review)
#         except Exception as e:
#             print(e)
    
#     # return reviewlist

    
# def url_sessions(urls, userAgents):
#     with requests.Session() as session:
#         session.headers.update({'User-Agent': userAgents[0]})
#         for url in urls:
#             # driver = webdriver.Chrome(ChromeDriverManager().install())
#             # driver.maximize_window()
#             # driver.get(url)
#             # time.sleep(10)
#             if url == 0:
#                 continue
#             pg = 1
#             while True:  # Loop to iterate through pages
#                 modified_url = f"{url}&pageNumber={pg}&sortBy=recent"
#                 max_tries = 21
#                 attempts = 0
#                 response = None
#                 while attempts < max_tries and not response:
#                     try:
#                         response = session.get(modified_url)
#                         if response.status_code == 200:
#                             print(f"Successfully fetched data from {modified_url}")
#                             extract_reviews(response.content)
#                             soup = BeautifulSoup(response.content, "html.parser")
#                             next_page = soup.find('li', class_= 'a-last')  # Checks for the 'Next' button
#                             last_page = soup.find("li", class_ = "a-disabled a-last")
#                             # print(next_page)
#                             # print(last_page)
#                             # if pg >= 2:
#                             #     if not next_page.find("li",{"class" : "a-disabled a-last"}):
#                             #         pg += 1
#                             #     else:
#                             #         raise StopIteration
#                             # next_page = soup.find("ul", {"class" : "a-pagination"})
#                             # if next_page.find("li", {"class" : "a-disabled a-last"}):
#                             #     # url = "https://www.amazon.in" + str(next_page.find('li', {'class' : 'a-last'}).find('a')['href'])
#                             #     raise StopIteration
#                             # else:
#                             #     pg += 1

#                             if next_page and 'a-disabled a-last' not in next_page['class']:  # If 'Next' button is not disabled
#                                 pg += 1  
#                             else:
#                                 raise StopIteration # No more pages, raise exception to break from the inner loop
#                             # if last_page:
#                             #     raise StopIteration
#                             # else:
#                             #     pg += 1
#                         break
#                     except RequestException as e:
#                         print(f"An error occurred: {e}")
#                     except StopIteration:  # Catch the exception to break from the outer loop
#                         break
#                     finally:
#                         if attempts < max_tries - 1:
#                             session.headers.update({'User-Agent': userAgents[attempts % len(userAgents)]})
#                         time.sleep(3)
#                     attempts += 1
#                 try:
#                     if response is None or 'a-disabled a-last' in next_page.get('class', []):
#                         break  # Break from the outer loop if no response or last page reached
#                 except AttributeError:
#                     break
#                 # driver.close()

# # def url_sessions(urls, userAgents):
# #     with requests.Session() as session:
# #         session.headers.update({'User-Agent':userAgents[0]})
# #         for url in urls:
# #             pg = 1
# #             while True:
# #                 modified_url = f"{url}&pageNumber={pg}&sortBy=recent"
# #                 max_tries = 21
# #                 attempts = 0
# #                 response = None
# #                 while attempts < max_tries and not response:
# #                     try:
# #                         response = session.get(modified_url)
# #                         if response.status_code == 200:
# #                             print(f"Successfully fetched data from {modified_url}")
# #                             extract_reviews(response.content)
# #                             break
# #                             # soup = BeautifulSoup(response.content, "html.parser")
# #                             # next_page = soup.find("li", {"class": 'a-last'})
# #                             # if next_page and 'a-disabled' not in next_page['class']:
# #                             #     pg+=1
# #                             # else:
# #                             #     break
# #                             # print(reviews)

# #                         break
# #                     except RequestException as e:
# #                         print(f"An error occurred: {e}")
# #                     finally:
# #                         if attempts < max_tries - 1:  
# #                             session.headers.update({'User-Agent': userAgents[attempts % len(userAgents)]})
# #                         time.sleep(0.100)
# #                     attempts += 1
# def main(user_input):
#     imageUrl, Stars, fiveStarReviewUrl, fourStarReviewUrl, threeStarReviewUrl, twoStarReviewUrl, oneStarReviewUrl = scraping_top_url(user_input)

# # print(Stars, fiveStarReviewUrl, fourStarReviewUrl, threeStarReviewUrl, twoStarReviewUrl, oneStarReviewUrl, sep="\n")

# # fiveStarReviewUrl = fiveStarReviewUrl.replace("#reviews-filter-bar", "&pageNumber=")
# # pg = 1
#     if fiveStarReviewUrl != 0:
#         fiveStarReviewUrl = fiveStarReviewUrl.replace("#reviews-filter-bar", "") # + f"&pageNumber={pg}" + f"&sortBy=recent"
#     else:
#         fiveStarReviewUrl = 0
#     # print(fiveStarReviewUrl)
#     if fourStarReviewUrl != 0:
#         fourStarReviewUrl = fourStarReviewUrl.replace("#reviews-filter-bar", "") # + f"&pageNumber={pg}" + f"&sortBy=recent"
#     else:
#         fourStarReviewUrl = 0

#     if threeStarReviewUrl != 0:
#         threeStarReviewUrl = threeStarReviewUrl.replace("#reviews-filter-bar", "") # + f"&pageNumber={pg}" + f"&sortBy=recent"
#     else:
#         threeStarReviewUrl = 0

#     if twoStarReviewUrl != 0:
#         twoStarReviewUrl = twoStarReviewUrl.replace("#reviews-filter-bar", "") # + f"&pageNumber={pg}" + f"&sortBy=recent"
#     else:
#         twoStarReviewUrl = 0

#     if oneStarReviewUrl != 0:
#         oneStarReviewUrl= oneStarReviewUrl.replace("#reviews-filter-bar", "") # + f"&pageNumber={pg}" + f"&sortBy=recent"
#     else:
#         oneStarReviewUrl = 0


#     userAgents = [
#             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
#             'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
#             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81',
#             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0',
#             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
#             'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0',
#             'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15',
#             'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0',
#             'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
#             'Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0',
#             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
#             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
#             'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
#             'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
#             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
#             'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
#             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
#             'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
#             'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0',
#             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188',
#             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'
#             ]

#     urls = []
#     urls.append(fiveStarReviewUrl)
#     urls.append(fourStarReviewUrl)
#     urls.append(threeStarReviewUrl)
#     urls.append(twoStarReviewUrl)
#     urls.append(oneStarReviewUrl)
#     # print(urls)
#     url_sessions(urls, userAgents)
#     df = pd.DataFrame(reviewlist)
#     df.to_json("reviews.json", index=False)
#     df.to_csv("reviews.csv", index=False)
#     reviewlist.clear()
#     return reviewlist, imageUrl, Stars

# if __name__ == "__main__":
#     x = input("Product: ")
#     main(x)
    

