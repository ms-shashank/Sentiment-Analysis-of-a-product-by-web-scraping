# Sentiment Analysis on Product Reviews

## Overview

This project performs sentiment analysis on product reviews collected from Amazon based on user input. The goal is to help users make informed decisions about products by analyzing the sentiment of reviews.

## Features

- **Input Collection**: Collects user input regarding the product of interest via a Streamlit frontend.
- **Data Scraping**: Scrapes product reviews and ratings from Amazon using web scraping techniques.
- **Data Processing**: Cleans and processes the scraped data to prepare it for sentiment analysis.
- **Sentiment Analysis**: Uses VADER (Valence Aware Dictionary and sEntiment Reasoner) for sentiment analysis of the reviews.
- **Visualization**: Plots a graph to visualize the distribution of positive, negative, and neutral reviews.
- **Decision Support**: Enables users to assess the sentiment analysis results to determine the quality and sentiment of the product based on collected reviews.

## Requirements

Ensure you have Python 3.6+ installed along with the following libraries:

```
requests
beautifulsoup4
pandas
numpy
nltk
matplotlib
seaborn
wordcloud
vaderSentiment
streamlit
plotly
```

Install the required packages using:

```
pip install -r requirements.txt
```

## Usage

1. **Setup Environment**:
   - Clone the repository.
   - Install dependencies using `pip install -r requirements.txt`.

2. **Run the Application**:
   - Launch the Streamlit application: `streamlit run fe.py`.
   - Enter the product details in the frontend to initiate data scraping and sentiment analysis.

3. **Interpret Results**:
   - View the sentiment analysis results in the form of a graph showing counts of positive, negative, and neutral reviews.
   - Use the results to make informed decisions about the product's quality and user sentiment.

## Contributing

Contributions are welcome! If you have suggestions, enhancements, or issues, please submit them via GitHub issues.
