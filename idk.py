from sentiBot import ultra_main
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
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
    trained_data, imageUrl, ratings = ultra_main(user_input)
    #print(trained_data.value_counts())
    #print(imageUrl)
    #print(ratings)
    return trained_data, imageUrl, ratings

form = st.form(key="input_form", clear_on_submit=True)
text = form.text_input("Enter an product name: ")
submit = form.form_submit_button(label="Search")

if submit:
    if not text:
        st.warning("Please enter an item/product to search", icon="⚠️")
    else:
        clear_data()
        sentiData, imageUrl, Ratings = run_script(text)
        # fig = sns.countplot(sentiData).set_title("Distribution of Sentiment")
        st.image(imageUrl)
        df = pd.read_csv("star_ratings.csv")
        fig = px.bar(df, x = "Star", y = "Percentage", title="Star Ratings Distribution")
        st.plotly_chart(fig, use_container_width=True)
        sentiment_counts = sentiData.value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']
        figure = px.bar(sentiment_counts, x="Sentiment", y = "Count", title="Sentiment Distribution")
        st.plotly_chart(figure, use_container_width=True)
        # fig, ax = plt.subplots(figsize=(8, 6))
        # sns.countplot(x=sentiData, ax=ax)
        # ax.set_title("Distribution of Sentiment")
        # # st.write(Ratings)
        # st.plotly_chart(fig, use_container_width=True)
        
# run_script()