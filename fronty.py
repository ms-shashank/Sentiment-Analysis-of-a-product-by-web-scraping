import streamlit as st
from prodUrlFetcher import top_product_url
from scrapy import scraping_top_url, scraping_rating_and_reviews
from reviewScrapper import url_sessions

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

st.set_page_config(
    page_title="Sentiment Analysis",
    page_icon="♾️",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title(":blue[Sentiment Analysis of a product]")

st.markdown("""
    <style>
div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
    font-size: 17px;

}
.big-font {
    font-size: 18px;
}
    </style>
    """, unsafe_allow_html=True)

form = st.form(key="input_form", clear_on_submit=True)
text = form.text_input("Enter an product name: ")
submit = form.form_submit_button(label="Search")

if submit:
    if not text:
        st.warning("Please enter an item/product to search", icon="⚠️")
    else:
        try:
            url = top_product_url(text)
            img, a, fiveStarUrl, fourStarUrl, threeStarUrl, twoStarUrl, oneStarUrl = scraping_rating_and_reviews(url)
            if fiveStarUrl != 0:
                fiveStarUrl = fiveStarUrl.replace("#reviews-filter-bar", "") # + f"&pageNumber={pg}" + f"&sortBy=recent"
            else:
                fiveStarUrl = 0
    # print(fiveStarReviewUrl)
            if fourStarUrl != 0:
                fourStarUrl = fourStarUrl.replace("#reviews-filter-bar", "") # + f"&pageNumber={pg}" + f"&sortBy=recent"
            else:
                fourStarUrl = 0

            if threeStarUrl != 0:
                threeStarUrl = threeStarUrl.replace("#reviews-filter-bar", "") # + f"&pageNumber={pg}" + f"&sortBy=recent"
            else:
                threeStarUrl = 0

            if twoStarUrl != 0:
                twoStarUrl = twoStarUrl.replace("#reviews-filter-bar", "") # + f"&pageNumber={pg}" + f"&sortBy=recent"
            else:
                twoStarUrl = 0

            if oneStarUrl != 0:
                oneStarUrl= oneStarUrl.replace("#reviews-filter-bar", "") # + f"&pageNumber={pg}" + f"&sortBy=recent"
            else:
                oneStarUrl = 0
                
            urls = []
            urls.append(fiveStarUrl)
            urls.append(fourStarUrl)
            urls.append(threeStarUrl)
            urls.append(twoStarUrl)  
            urls.append(oneStarUrl)
            
            url_sessions(url, userAgents)
            st.image(img)
            #st.write(b, unsafe_allow_html = True)
        except Exception as e:
            st.error(f"An Error occured: {e}")
        # url = scraping_top_url(text)
        # st.write(url)
