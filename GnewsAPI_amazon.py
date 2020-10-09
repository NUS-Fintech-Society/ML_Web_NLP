import requests
import json
import pandas as pd
import datetime
import time
import nltk
import string
from dateutil import parser
from datetime import date

exclude = set(string.punctuation)

def preprocess_text(review):
    index = review.find(" - ")
    review = review[:index] #Remove source of article
    for i in review:
        if i in exclude:
            review = review.replace(i,"") #Remove punctuation
    review = review + "." #Adding fullstop
    return review

url = "https://google-news.p.rapidapi.com/v1/search"
headers = {
'x-rapidapi-host': "google-news.p.rapidapi.com",
'x-rapidapi-key': "" #Change to your API Key
}

start_date = datetime.date(2020, 1, 1) #(year, month, day)
counter = 0
while start_date < date.today():
    counter += 1
    end_date = start_date + datetime.timedelta(days = 7) #End of week
    start_date_str = str(start_date)
    end_date_str = str(end_date)
    querystring = {"country":"US","lang":"en","q":"amazon", "from":start_date_str, "to":end_date_str}
    response_amazon = requests.request("GET", url, headers=headers, params=querystring)

    with open('amazon_titles.json', 'w') as outfile:
        outfile.write(response_amazon.text)

    ls_amazon_titles = []
    ls_amazon_date = []
    with open('amazon_titles.json') as json_file:
        data = json.load(json_file)
        for article in data["articles"]:
            ls_amazon_titles.append(article["title"])
            date_str = article["published"]
            article_date = datetime.datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
            ls_amazon_date.append(article_date)

    amazon_titles = pd.DataFrame({"Date": ls_amazon_date, "Review":ls_amazon_titles})
    amazon_titles["Year"] = amazon_titles["Date"].apply(lambda x: x.isocalendar()[0]) #Extracting year
    amazon_titles["Week"] = amazon_titles["Date"].apply(lambda x: x.isocalendar()[1]) #Extracting Week
    amazon_titles["Review"] = amazon_titles["Review"].apply(lambda x: preprocess_text(x))

    titles = pd.read_csv("amazon_titles.csv")
    titles_concat = pd.concat([titles, amazon_titles], axis = 0)
    titles_concat.to_csv("amazon_titles.csv", index = False)

    start_date = end_date #Next week data
    if counter%5 == 0:
        time.sleep(3600)
