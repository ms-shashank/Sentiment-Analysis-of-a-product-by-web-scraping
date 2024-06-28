from sentiBot import ultra_main
import streamlit as st
import seaborn as sns
import pandas as pd
import os
import plotly.express as px

st.set_page_config(
    page_title="Sentiment Analysis",
    page_icon="♾️",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title(":blue[Sentiment Analysis of a Product]")
st.divider()

def clear_data():
    empty_df = pd.DataFrame()
    if not os.path.exists("reviews.csv"):
        with open("reviews.csv", "w", newline="") as file:
            pass
    else:
        empty_df.to_csv("reviews.csv", index=False)


def run_script(user_input):
    trained_data, imageUrl, ratings, figs = ultra_main(user_input)
    return trained_data, imageUrl, ratings, figs 


form = st.form(key="input_form", clear_on_submit=True)
text = form.text_input("Enter a product name: ")
submit = form.form_submit_button(label="Search")

if submit:
    if not text:
        st.warning("Please enter an item/product to search", icon="⚠️")
    else:
        clear_data()
        sentiData, imageUrl, Ratings, figs = run_script(text)
        st.image(imageUrl)
        
        st.divider()
        
        st.subheader("Sentiment Analysis")
        df = pd.read_csv("star_ratings.csv")
        fig = px.bar(df, x="Star", y="Percentage", title="Star Ratings Distribution")
        st.plotly_chart(fig, use_container_width=True)
        
        sentiment_counts = sentiData.value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']
        figure = px.bar(sentiment_counts, x="Sentiment", y="Count", title="Sentiment Distribution")
        st.plotly_chart(figure, use_container_width=True)
        
        st.divider()
        
        st.subheader("Word Clouds")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.pyplot(figs[0])
        with col2:
            st.pyplot(figs[1])
        with col3:
            st.pyplot(figs[2])
            
            
#------------------------------------------------------------------------------------------------------------------------------------------------------            
        # with col1:
        #     st.image(wordcloud_pos, caption='Positive Word Cloud', width=300)
        # with col2:
        #     st.image(wordcloud_neg, caption='Negative Word Cloud', width=300)
        # with col3:
        #     st.image(wordcloud_neu, caption='Neutral Word Cloud', width=300)
            
# from sentiBot import ultra_main
# import streamlit as st
# import seaborn as sns
# import matplotlib.pyplot as plt
# import pandas as pd
# import os
# import plotly.express as px
# from wordcloud import WordCloud
# from nltk.corpus import stopwords
# import nltk

# # nltk.download("stopwords")
# # nltk_stpwd = stopwords.words("english")


# st.set_page_config(
#     page_title="Sentiment Analysis",
#     page_icon="♾️",
#     layout="centered",
#     initial_sidebar_state="auto",
# )

# st.title(":blue[Sentiment Analysis of a Product]")
# st.divider()
# # st.set_option('deprecation.showPyplotGlobalUse', False)

# def clear_data():
#     empty_df = pd.DataFrame()
#     if not os.path.exists("reviews.csv"):
#         with open("reviews.csv", "w", newline="") as file:
#             pass
#     else:
#         empty_df.to_csv("reviews.csv", index=False)


# def run_script(user_input):
#     trained_data, imageUrl, ratings, wordcloud_pos, wordcloud_neg, wordcloud_neu = ultra_main(user_input)
#     #print(trained_data.value_counts())
#     #print(imageUrl)
#     #print(ratings)
#     print(wordcloud_pos)
#     return trained_data, imageUrl, ratings, wordcloud_pos, wordcloud_neg, wordcloud_neu 


# form = st.form(key="input_form", clear_on_submit=True)
# text = form.text_input("Enter an product name: ")
# submit = form.form_submit_button(label="Search")

# if submit:
#     if not text:
#         st.warning("Please enter an item/product to search", icon="⚠️")
#     else:
#         clear_data()
#         sentiData, imageUrl, Ratings, wordcloud_pos, wordcloud_neg, wordcloud_neu = run_script(text)
#         # fig = sns.countplot(sentiData).set_title("Distribution of Sentiment")
#         st.image(imageUrl)
#         df = pd.read_csv("star_ratings.csv")
#         fig = px.bar(df, x = "Star", y = "Percentage", title="Star Ratings Distribution")
#         st.plotly_chart(fig, use_container_width=True)
#         sentiment_counts = sentiData.value_counts().reset_index()
#         sentiment_counts.columns = ['Sentiment', 'Count']
#         figure = px.bar(sentiment_counts, x="Sentiment", y = "Count", title="Sentiment Distribution")
#         st.plotly_chart(figure, use_container_width=True)
#         # wordcloud = WordCloud(height=2000, width=2000, stopwords=set(stopwords.words('english')), background_color='white')
#         # wordcloud = wordcloud.generate(wordcloud_pos)
#         # st.pyplot(plt.imshow(wordcloud_pos))
#         # st.pyplot(plt.imshow(wordcloud_neg))
#         # st.pyplot(plt.imshow(wordcloud_neu))
#         plt.imshow(wordcloud_pos)
#         plt.axis("off")
#         plt.show()
#         st.pyplot()
#         plt.imshow(wordcloud_neg)
#         plt.axis("off")
#         plt.show()
#         st.pyplot()
#         plt.imshow(wordcloud_neu)
#         plt.axis("off")
#         plt.show()
#         st.pyplot()
#         # fig, ax = plt.subplots(figsize=(8, 6))
#         # sns.countplot(x=sentiData, ax=ax)
#         # ax.set_title("Distribution of Sentiment")
#         # # st.write(Ratings)
#         # st.plotly_chart(fig, use_container_width=True)
        
# # run_script("Iphone 15 pro max")

#----------------------------------------------------------------------------------------------------------------

