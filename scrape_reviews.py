from scrapy import scraping_rating_and_reviews, scraping_top_url
from bs4 import BeautifulSoup
import requests
import time
import csv

Stars, fiveStarReviewUrl, fourStarReviewUrl, threeStarReviewUrl, twoStarReviewUrl, oneStarReviewUrl = scraping_top_url()

print(Stars, fiveStarReviewUrl, fourStarReviewUrl, threeStarReviewUrl, twoStarReviewUrl, oneStarReviewUrl, sep="\n")
