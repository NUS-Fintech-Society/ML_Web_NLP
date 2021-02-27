import csv
import requests
import json
import pandas as pd
import time
import nltk
import string
from dateutil import parser
from datetime import date, datetime, timedelta
from apipool import ApiKey, ApiKeyManager

import config

def preprocess_text(text):
    """Removing source and punctuations from title"""

    text = " ".join(text.split("-")[:-1]) # Remove source of article
    text = text.translate(str.maketrans('', '', string.punctuation)) # Remove punctuation in title
    text = text.strip() + "." # Adding fullstop to title

    return text

def extract_news(company):
    """Extract News from Google News API"""

    # Initialise api request variables
    url = "https://google-news.p.rapidapi.com/v1/search"
    headers = {
    'x-rapidapi-host': "google-news.p.rapidapi.com",
    'x-rapidapi-key': api_key
    }

    # Initialise variables
    extract_start_date = start_date

    while extract_start_date < end_date:
        extract_end_date = extract_start_date + timedelta(days=7) # End of week

        # Make api call
        query_string = {"country":"US", "lang":"en", "q":company, "from":str(extract_start_date), "to":str(extract_end_date)}
        response = requests.request("GET", url, headers=headers, params=query_string)
        response_text = json.loads(response.text)

        # Check if api limit has been reached
        if 'message' in response_text:
            print("API limit reached, sleeping for 1 hour")
            time.sleep(3600)
            continue

        print("Progress: Extracted {} for the time period {} to {}".format(company, extract_start_date, extract_end_date))
        # Save query results progressively
        with open(output_path, 'a', newline='') as f:
            writer = csv.writer(f)

            for article in response_text['articles']:
                title = preprocess_text(article["title"]).encode('utf-8')
                date = datetime.strptime(article["published"], '%a, %d %b %Y %H:%M:%S %Z')
                date_posted = date.strftime('%Y-%m-%d')
                year = date.isocalendar()[0] # Extracting year
                week = date.isocalendar()[1] # Extracting week
                writer.writerow([company, title, date_posted, year, week])

        extract_start_date = extract_end_date # Next week data

# class RapidApiKey(ApiKey):
#     def __init__(self,
#                  api_key)
#         self.api_key = api_key

#     def get_primary_key(self):
#         return self.api_key

#     def test_usable(self, api_key):
#         query_string = {"country":"US", "lang":"en", "q":company, "from":str(extract_start_date), "to":str(extract_end_date)}
#         response = requests.request("GET", url, headers=headers, params=query_string)
#         response_text = json.loads(response.text)

#         # Check if api limit has been reached
#         if 'message' in response_text:
#             return False
#         else:
#             return True

# USE https://pypi.org/project/apipool/#description

if __name__ == "__main__":
    # Set parameters (year, month, day)
    start_date = date(2020, 2, 12)
    end_date = date(2020, 6, 30)
    print("Start date: " + start_date.strftime('%Y-%m-%d'))
    print("End date: " + end_date.strftime('%Y-%m-%d'))
    today = date.today()

    # TODO: Edit the program to allow multiple API keys and concurrent retrieval
    # api_keys = config.API_KEYS
    # api_keys_list = [
    #     RapidApiKey(**api_key)
    #     for api_key in api_keys
    # ]
    # manager = ApiKeyManager(apikey_list=api_keys_list)

    api_key = config.API_KEYS[0]

    companies_path = 'companies.txt'
    output_path = 'initialise_news {}.csv'.format(today)

    # Write header for output file
    col_names = ['company_name', 'title', 'date_posted', 'year', 'week'] # 'score'
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(col_names)

    # Load companies for extraction
    companies = open(companies_path).read().split()
    
    # Extract news for all companies
    for company in companies:
        print("Extracting news: " + company)
        extract_news(company)
