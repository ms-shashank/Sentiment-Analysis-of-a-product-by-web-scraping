from sentiBot import ultra_main
import streamlit as st

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
        sentiData, imageUrl, Ratings = run_script(text)
        st.write(Ratings)
        
# run_script()