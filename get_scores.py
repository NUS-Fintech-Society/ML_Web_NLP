# import nltk
# nltk.download('vader_lexicon')

from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd

def get_scores(data):
    """Returns Sentiment Analysis Scores"""
    
    sia = SentimentIntensityAnalyzer()

    for index, row in data.iterrows():
        score = sia.polarity_scores(row['title'])
        print(score['compound'])


if __name__ == "__main__":
    data = pd.read_csv("test.csv", encoding='unicode_escape')
    
    get_scores(data)
