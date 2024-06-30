# from justForMyExample import main
from reviewScrapper import main
import pandas as pd
# import numpy as np
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
# from gensim import corpora, models
# import gensim
import nltk
# import plotly.express as px
import matplotlib.pyplot as plt
import re
# import pyLDAvis
# import pyLDAvis.gensim
import string
from nltk.stem import PorterStemmer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from collections import Counter
import seaborn as sns
from wordcloud import WordCloud
from io import BytesIO

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
    
    wordcloud = WordCloud(stopwords = set(stopwords.words('english')), background_color='white', min_font_size= 10, max_words=20)

    # positive_text = ' '.join(train.loc[train['sentiment'] == "Positive", "cleaned"].tolist())
    # wordcloud_positive = wordcloud.generate(positive_text)
    # pos_img = BytesIO()
    # wordcloud_positive.to_image().save(pos_img, format='PNG')
    # pos_img.seek(0)

    # # Generate and save negative word cloud
    # negative_text = ' '.join(train.loc[train['sentiment'] == "Negative", "cleaned"].tolist())
    # wordcloud_negative = wordcloud.generate(negative_text)
    # neg_img = BytesIO()
    # wordcloud_negative.to_image().save(neg_img, format='PNG')
    # neg_img.seek(0)

    # # Generate and save neutral word cloud
    # neutral_text = ' '.join(train.loc[train['sentiment'] == "Neutral", "cleaned"].tolist())
    # wordcloud_neutral = wordcloud.generate(neutral_text)
    # neu_img = BytesIO()
    # wordcloud_neutral.to_image().save(neu_img, format='PNG')
    # neu_img.seek(0)
    figs = []
    
    wordcloud = wordcloud.generate(' '.join(train.loc[train['sentiment']=='Positive','cleaned'].tolist()))
    fig, ax = plt.subplots(figsize=(15, 15))
    ax.set_facecolor('black')
    plt.imshow(wordcloud)
    plt.title("Positive words", fontsize=55, color = "black", pad=40)
    plt.axis('off')
    plt.show()
    figs.append(fig)
    
    wordcloud_neg = wordcloud.generate(' '.join(train.loc[train['sentiment']=='Negative','cleaned'].tolist()))
    figOne, ax = plt.subplots(figsize=(15, 15))
    ax.set_facecolor('black')
    plt.imshow(wordcloud_neg)
    plt.title("Negative words", fontsize=55, color = "black", pad=40)
    plt.axis('off')
    plt.show()
    figs.append(figOne)
    
    
    wordcloud_neu = wordcloud.generate(' '.join(train.loc[train['sentiment']=='Neutral','cleaned'].tolist()))
    figTwo, ax = plt.subplots(figsize=(15, 15))
    ax.set_facecolor('black')
    plt.imshow(wordcloud_neu)
    plt.title("Neutral words", fontsize=60, color = "black", pad=40)
    plt.axis('off')
    plt.show()
    figs.append(figTwo)

    return train['sentiment'], imageUrl, rating, figs 
    # return train['sentiment'], imageUrl, rating, pos_img, neg_img, neu_img
    
    # return train['sentiment'], imageUrl, rating, wordcloud_positive, wordcloud_negative, wordcloud_nutral    

    sns.countplot(train['sentiment']).set_title("Distribution of Sentiment")
    plt.show()
    plt.pause(3)
    plt.close()

if __name__ == "__main__":
    x = input("Product Name: ")
    ultra_main(x)
    