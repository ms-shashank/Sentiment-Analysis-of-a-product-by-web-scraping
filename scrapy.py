from prodUrlFetcher import top_product_url
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt

userAgents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
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

rating = []
reviews = []
fiveStarRating = []
fourStarRating = []
threeStarRating = []
twoStarRating = []
oneStarRating = []

def scraping_top_url():
    user_input = input("Enter a product: ")
    url = top_product_url(user_input)
    print(url)
    star, fiveStarReview, fourStarReview, threeStarReview, twoStarReview, oneStarReview = scraping_rating_and_reviews(url)
    return star, fiveStarReview, fourStarReview, threeStarReview, twoStarReview, oneStarReview      
    # scraping_reviews(url)

def scraping_rating_and_reviews(rating_url):
    
    max_tries = 21
    attempts = 0
    response = None

    fiveStarUrl = 0
    fourStarUrl = 0 
    threeStarUrl = 0
    twoStarUrl = 0
    oneStarUrl = 0
    # while True:
    #     for i in userAgents:
    #         response = requests.get(rating_url, headers={'User-Agent': i})
    #         if response.status_code == 200:
    #             break
    #     if response.ok:
    #         break
    #     else:
    #         continue
    while attempts < max_tries and not response:
        for i in userAgents:
            try:
                response = requests.get(rating_url, headers={'User_Agent': i})
                if response.status_code == 200:
                    # print(i)
                    break
            except requests.RequestException as e:
                print(f"An error occurred: {e}")
            time.sleep(0.100)
        attempts += 1
    
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        
    #     stars =  soup.find_all("a", class_ = "a-size-base a-link-normal")
    #     print(stars)
    #     for precentage in stars:
    #         rating.append(precentage.get_text())
    #     print(rating)
    # else:
    #     print("Failed to retrieve the ratings after maximum retries.")

        x = soup.find_all("td", class_ = "a-text-right a-nowrap a-nowrap")
        for td in x:
            rating_percentage = td.find_all("a", class_ = "a-size-base a-link-normal")
            zero_percentage = td.find_all("span", class_ = "a-size-base")
            for zero in zero_percentage:
                rating.append(zero.get_text())
            for percentage in rating_percentage:
                rating.append(percentage.get_text())
        # print(rating)

        fiveStarReviewLink = soup.find_all('a', {'class': "a-size-base a-link-normal"})
        #print(fiveStarReviewLink)
        if fiveStarReviewLink:

            # fiveStarUrl = ""
            # fourStarUrl = ""
            # threeStarUrl = ""
            # twoStarUrl = ""
            # oneStarUrl = ""

            # itterate through the html parse and i can handle everything/retrieve any data from the html 
            for hyperlinks in fiveStarReviewLink:
                # every parameter till query string separater "?" it is same so we will search only for those hyper links 
                if 'ref=acr_dp_hist_5?' in hyperlinks['href']:
                    #print(hyperlinks['href'])
                    fiveStar = hyperlinks['href']
                    fiveStarUrl = 'https://www.amazon.in' + fiveStar


                if 'ref=acr_dp_hist_4?' in hyperlinks['href']:
                    fourStar = hyperlinks['href']
                    fourStarUrl = 'https://www.amazon.in' + fourStar


                if 'ref=acr_dp_hist_3?' in hyperlinks['href']:
                    threeStar = hyperlinks['href']
                    threeStarUrl = 'https://www.amazon.in' + threeStar


                if 'ref=acr_dp_hist_2?' in hyperlinks['href']:
                    twoStar = hyperlinks['href']
                    twoStarUrl = 'https://www.amazon.in' + twoStar


                if 'ref=acr_dp_hist_1?' in hyperlinks['href']:
                    oneStar = hyperlinks['href']
                    oneStarUrl = 'https://www.amazon.in' + oneStar
                    break


        # fiveStarUrl = 'https://www.amazon.in' + fiveStar
        # fourStarUrl = 'https://www.amazon.in' + fourStar
        # threeStarUrl = 'https://www.amazon.in' + threeStar
        # twoStarUrl = 'https://www.amazon.in' + twoStar
        # oneStarUrl = 'https://www.amazon.in' + oneStar
        
        # print(fiveStarUrl)
        # print(fourStarUrl)
        # print(threeStarUrl)
        # print(twoStarUrl)
        # print(oneStarUrl)
    else:
        print("Response not recivied/Satisifyed")


    # To Convert the [5, 4, 3, 2, 1] to []
    # df = pd.DataFrame(rating, rows=["Stars"])
    # df.to_csv("Ratings_of_prod", index=False)


    # Convert percentages to float for graphing
    star_percentages = [float(rates.strip('%')) for rates in rating]

    st = ['5 stars', '4 stars', '3 stars', '2 stars', '1 star']

    with open('star_ratings.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Star', 'Percentage'])
        for star, percentage in zip(st, star_percentages):
            writer.writerow([star, percentage])

    plt.bar(st, star_percentages, color="skyblue")
    plt.xlabel("Stars")
    plt.ylabel("percentage")
    plt.title("Star Ratings")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(3)
    plt.close()

    return rating, fiveStarUrl, fourStarUrl, threeStarUrl, twoStarUrl, oneStarUrl

        # Initialize a dictionary with the expected order of star ratings
#     ratings_dict = {
#         '5 star': None,
#         '4 star': None,
#         '3 star': None,
#         '2 star': None,
#         '1 star': None
#     }

#     x = soup.find_all("td", class_="a-text-right a-nowrap a-nowrap")

#     for td in x:
#     # Find all percentages for non-zero ratings
#         rating_percentage = td.find_all("a", class_="a-size-base a-link-normal")
#         for percentage in rating_percentage:
#             stars = percentage.find_previous("td").get_text()
#             ratings_dict[stars] = percentage.get_text()

#     # Find all percentages for zero ratings
#         zero_handling = td.find_all("span", class_="a-size-base")
#         for zero in zero_handling:
#             stars = zero.find_previous("td").get_text()
#             ratings_dict[stars] = zero.get_text() if zero.get_text() else "0%"

#     # print(ratings_dict)
# # Convert the ratings dictionary to a list while maintaining the order
#     ratings_list = [ratings_dict[key] if ratings_dict[key] is not None else "0%" for key in ratings_dict]
#     final_ratings = ratings_list[5:]
#     print(final_ratings)



        
# def scraping_reviews(reviewing_url):
#     max_tries = 21
#     attempts = 0
#     response = None

#     while attempts < max_tries and not response:
#         for i in userAgents:
#             try:
#                 response = requests.get(reviewing_url, headers={'User_Agent': i})
#                 if response.status_code == 200:
#                     break
#             except requests.RequestException as e:
#                 print(f"An error occurred: {e}")
#             time.sleep(1)
#         attempts += 1
    
#     if response.ok:
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # i am taking the a tag with the class name and will iterate through out this and i will find out many classes under this
#         fiveStarReviewLink = soup.find_all('a', {'class': "a-size-base a-link-normal"})
#         #print(fiveStarReviewLink)
#         if fiveStarReviewLink:
#             # itterate through the html parse and i can handle everything/retrieve any data from the html 
#             for hyperlinks in fiveStarReviewLink:
#                 # every parameter till query string separater "?" it is same so we will search only for those hyper links 
#                 if 'ref=acr_dp_hist_5?' in hyperlinks['href']:
#                     #print(hyperlinks['href'])
#                     fiveStar = hyperlinks['href']
#                 if 'ref=acr_dp_hist_4?' in hyperlinks['href']:
#                     fourStar = hyperlinks['href']
#                 if 'ref=acr_dp_hist_3?' in hyperlinks['href']:
#                     threeStar = hyperlinks['href']
#                 if 'ref=acr_dp_hist_2?' in hyperlinks['href']:
#                     twoStar = hyperlinks['href']
#                 if 'ref=acr_dp_hist_1?' in hyperlinks['href']:
#                     oneStar = hyperlinks['href']
#                     break

#         fiveStarUrl = 'https://www.amazon.in' + fiveStar
#         fourStarUrl = 'https://www.amazon.in' + fourStar
#         threeStarUrl = 'https://www.amazon.in' + threeStar
#         twoStarUrl = 'https://www.amazon.in' + twoStar
#         oneStarUrl = 'https://www.amazon.in' + oneStar
        
#         print(fiveStarUrl)
#         print(fourStarUrl)
#         print(threeStarUrl)
#         print(twoStarUrl)
#         print(oneStarUrl)


# scraping_top_url()