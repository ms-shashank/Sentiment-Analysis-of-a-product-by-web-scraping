# from justForMyExample import main
from reviewScrapper import main
import pandas as pd
import numpy as np
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from gensim import corpora, models
import gensim
import nltk
import plotly.express as px
import matplotlib.pyplot as plt
import re
import pyLDAvis
import pyLDAvis.gensim
import string
from nltk.stem import PorterStemmer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter
import seaborn as sns

def ultra_main(user_input):
    reviewlist, imageUrl, rating = main(user_input)
    print(imageUrl)
    print(rating)
    # print(call)

    df = pd.read_csv("reviews.csv", sep = ",")
    train = df

    def clean_text(text):
        ps = PorterStemmer() # The PorterStemmer object from the nltk library. This object will be used to perform stemming, which reduces words to their root form
        text1 = re.sub(r"https?:\/\/.*[\r\n]*", "", text) # to remove the urls from the data
        text_cleaned = " ".join([x for x in text1 if x not in string.punctuation]) # removes the punctuation
        text_cleaned = text_cleaned.lower() # converted to lowercase (for uniformity as the case letters are not usually important in text processing)
        text_cleaned = text_cleaned.split(" ") # Splited by spaces (tokens)
        text_tokens = [token for token in text_cleaned if token not in stopwords] #removes stopwords from text_cleaned(like is, the, and , etc..)
        stem_words = [ps.stem(stem) for stem in text_tokens] # Each token is stemmed (reduces words to their base forms)
        text = " ".join(stem_words)
        text_cleaned = re.sub(' +', ' ', text) # replaces consective spaces with single spaces
        return text_cleaned

    train['cleaned'] = train['Review Body'].apply(lambda x: re.sub("\n+", " ", str(x)) if pd.notnull(x) else x)
    # print(train['cleaned'].head())

    # train['cleaned'].tolist()

    train["cleaned"] = train["cleaned"].str.replace(r"\s+", " ", regex=True)
    train["cleaned"] = train["cleaned"].str.replace(r"[^\w\s#@/:%.,_-]", "", flags=re.UNICODE) #removing emojis from the data
    train["cleaned"] = train["cleaned"].replace(r'\.', ' ', regex=True)
    train["clenaed"] = train["cleaned"].replace(r",", ".", regex=True)
    # print(train['cleaned'].tolist())

    train["cleaned"] = train['cleaned'].apply(lambda x: re.sub(r"#[\w]+", '', str(x)) if pd.notnull(x) else x) #to remove # words (#words)
    train["cleaned"] = train['cleaned'].apply(lambda cleaned_review: "".join([x for x in str(cleaned_review) if x not in string.punctuation]))
    train["cleaned"] = train['cleaned'].apply(lambda x: x.lower())

    def removePunct(text):
        text = text.translate(str.maketrans({key: " {0} ".format(key) for key in string.punctuation}))
        text_cleaned = "".join([x for x in text if x not in string.punctuation])
        text_cleaned = re.sub(r'[^\x00-\x7F]+', ' ', text_cleaned) # to remove asscii characters
        text_cleaned = re.sub(r'\s+', ' ', text_cleaned).strip()
        return text_cleaned

    train["cleaned"] = train['cleaned'].apply(lambda x:removePunct(x))
    # print(train["cleaned"].head())

    tokenizer = RegexpTokenizer(r"\w+")
    train1 = train.cleaned[0]
    tokens = tokenizer.tokenize(train1.lower())
    # print('{} characters in string vs {} words in a list'.format(len(train1), len(tokens)))
    # print(tokens)

    nltk.download("stopwords")
    nltk_stpwd = stopwords.words("english")
    # print(nltk_stpwd)

    stopped_tokens = [token for token in tokens if not token in nltk_stpwd]
    # print(stopped_tokens)

    sb_stemmer = SnowballStemmer('english')
    stemmed_tokens = [sb_stemmer.stem(token) for token in stopped_tokens]

    # Implementing my Sentiment Analysis model
    def sentiBotAnalyzer(input):
        sentiment = SentimentIntensityAnalyzer()
        statement = sentiment.polarity_scores(input)
        return statement['pos'], statement['neg'], statement['neu'], statement['compound']

    def analyzeCompound(get_text):
        x, y, z, comp = sentiBotAnalyzer(get_text)
        if comp < 0:
            return "Negative"
        elif 0 <= comp <= 0.4:
            return "Neutral"
        elif 0.4 < comp:
            return "Positive"

    train['sentiment'] = train['cleaned'].apply(lambda x: analyzeCompound(x))
    # print(train['sentiment'].head(10))
    # print(train['sentiment'].value_counts())
    
    return train['sentiment'], imageUrl, rating

    sns.countplot(train['sentiment']).set_title("Distribution of Sentiment")
    plt.show()
    plt.pause(3)
    plt.close()

if __name__ == "__main__":
    ultra_main()
    