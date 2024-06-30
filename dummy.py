from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from dataclasses import dataclass
from rich import print

@dataclass
class Item:
    asin: str
    # title: str
    # price: str
    review_content: str

def get_html(page, asin):
    # url = f"https://www.amazon.in/product-reviews/{asin}/ref=cm_cr_arp_d_viewopt_sr?ie=UTF8&filterByStar=all_stars&reviewerType=all_reviews&pageNumber=1"
    url = f"https://www.amazon.in/product-reviews/{asin}/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&filterByStar=all_stars&reviewerType=all_reviews&pageNumber=2"
    print(url)
    page.goto(url)
    html = HTMLParser(page.content())
    print(html)
    return html

# def parse_html(html, asin):
#     item = Item(
#         asin = asin, 
#         # title = html.css_first("span#productTitle").text(strip=True),
#         # # price = html.css_first("span.a-offscreen").text(strip=True)
#         # review_content = html.css_first("span.a-size-base.review-text.review-text-content").text(strip=True)
#         review_content = html.css_first("a.a-size-base.a-link-normal.review-title.a-color-base.review-title-content.a-text-bold").text(strip=True)
#     )
#     # print(html.css_first("title").text())
#     # print(asin)
#     return item

def parse_html(html, asin):
    reviews = html.css("span.a-size-base.review-text.review-text-content")
    items = []
    for review in reviews:
        item = Item(
            asin = asin,
            review_content=review.text(strip=True)
        )
        items.append(item)
    return items

    # item = Item(
    #     asin=asin,
    #     review_content=html.css_first("span.a-size-base.review-text.review-text-content").text(strip=True)
    # )
    # return item

    
def run():
    asin = "B0B296NTFV"
    pw = sync_playwright().start()
    browser = pw.chromium.launch()
    page = browser.new_page()
    html = get_html(page, asin)
    product = parse_html(html, asin)
    print(product)

def main():
    run()


if __name__ == "__main__": 
    main()