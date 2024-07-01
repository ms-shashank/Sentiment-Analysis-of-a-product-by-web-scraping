from sentiBot import ultra_main
import streamlit as st
import pandas as pd
import os
import plotly.express as px
import uuid
from reviewScrapper import main

st.set_page_config(
    page_title="Sentiment Analysis",
    page_icon="♾️",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title(":blue[Sentiment Analysis of a Product]", anchor=False)
st.divider()

# Initialize session state variables
if 'sentiData' not in st.session_state:
    st.session_state['sentiData'] = None
if 'imageUrl' not in st.session_state:
    st.session_state['imageUrl'] = None
if 'Ratings' not in st.session_state:
    st.session_state['Ratings'] = None
if 'figs' not in st.session_state:
    st.session_state['figs'] = None
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = str(uuid.uuid4())  # Generate a unique session ID

# def get_review_filename():
#     return f"reviews_{st.session_state.session_id}.csv"

# def clear_data():
#     empty_df = pd.DataFrame()
#     filename = get_review_filename()
#     if not os.path.exists(filename):
#         with open(filename, "w", newline="") as file:
#             pass
#     else:
#         empty_df.to_csv(filename, index=False)

def run_script(user_input):
    session_id = st.session_state.session_id
    trained_data, imageUrl, ratings, figs = ultra_main(user_input, session_id)
    return trained_data, imageUrl, ratings, figs 

def clear_session_state():
    st.session_state.sentiData = None
    st.session_state.imageUrl = None
    st.session_state.Ratings = None
    st.session_state.figs = None
    
form = st.form(key="input_form", clear_on_submit=True)
text = form.text_input("Enter a product name: ")
submit = form.form_submit_button(label="Search")


if submit:
    if not text:
        st.warning("Please enter an item/product to search", icon="⚠️")
    else:
        with st.spinner(f"Searching for reviews for **{text}**..."):
            # clear_data()
            try:
                clear_session_state()
                st.session_state['sentiData'], st.session_state['imageUrl'], st.session_state['Ratings'], st.session_state['figs'] = run_script(text)
            except Exception as e:
                st.error(f"An error occured {e}")
                
if st.session_state['sentiData'] is not None:
    col1, col2 = st.columns(2)
    with col1:
        st.image(st.session_state['imageUrl'])
    with col2:
        df = pd.read_csv(f"reviews_{st.session_state.session_id}.csv", sep=",")
        st.write(f'# <span class=big-font>Found `{len(df)}` reviews</span>', unsafe_allow_html=True)
             
    st.divider()
    
    st.header("Sentiment Analysis")
    df = pd.read_csv(f"star_ratings_{st.session_state.session_id}.csv")
    fig = px.bar(df, x="Star", y="Percentage", title="Star Ratings Distribution")
    st.plotly_chart(fig, use_container_width=True)
    
    sentiment_counts = st.session_state['sentiData'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']
    figure = px.bar(sentiment_counts, x="Sentiment", y="Count", title="Sentiment Distribution")
    st.plotly_chart(figure, use_container_width=True)
    
    st.divider()
    
    st.header("Word Clouds")
    col3, col4, col5 = st.columns(3)
    with col3:
        st.pyplot(st.session_state['figs'][0])
    with col4:
        st.pyplot(st.session_state['figs'][1])
    with col5:
        st.pyplot(st.session_state['figs'][2])

            