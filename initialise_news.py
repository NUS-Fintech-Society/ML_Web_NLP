import csv
import requests
import json
import pandas as pd
import time
import nltk
import string
import os
from dateutil import parser
from datetime import date, datetime, timedelta

import config

def print_banner(text, length=70):
    print(">"*length)
    print(text)
    print("<"*length)

def print_line(text, length=70):
    side_length = int((50-len(text))/2)
    print("="*side_length + text + "="*side_length)

def preprocess_text(text):
    """Removing source and punctuations from title"""

    text = " ".join(text.split("-")[:-1]) # Remove source of article
    text = re.sub(' +', ' ', text) # Remove additional whitespace

    return text

def get_extract_end_date(extract_start_date, end_date):
    """Get extract end date based on standardisation rules"""

    # To query in the same ISO week only
    if extract_start_date.weekday() == 6: # 6 refers to Sunday index
        extract_end_date = extract_start_date + timedelta(days=7) # End of week
    else:
        days_to_sunday = timedelta((6 - extract_start_date.weekday()) % 7)
        extract_end_date = extract_start_date + days_to_sunday # End of week
    
    # Ensure extract end date does not exceed end date
    if extract_end_date > end_date:
        extract_end_date = end_date
    
    return extract_end_date

def extract_news(company):
    """Extract News from Google News API"""

    # Initialise api request variables
    url = "https://google-news.p.rapidapi.com/v1/search"
    api_key_index = 0 # Start with first key

    # Initialise variables
    extract_start_date = start_date # Start with first day

    while extract_start_date < end_date:
        # Initialise api request key (for rotation)
        headers = {
            'x-rapidapi-host': "google-news.p.rapidapi.com",
            'x-rapidapi-key': api_keys[api_key_index]
            }

        extract_end_date = get_extract_end_date(extract_start_date, end_date)

        # Make api call
        query_string = {"country":"US", "lang":"en", "q":company, 
            "from":str(extract_start_date), "to":str(extract_end_date)
            }
        response = requests.request("GET", url, headers=headers, 
            params=query_string)
        response_text = json.loads(response.text)

        # Check if api limit has been reached
        if 'message' in response_text:
            # Update api key index
            if api_key_index + 1 < len(api_keys):
                new_api_key_index = api_key_index + 1
                print_line("API limit reached for API key index {}, switching to {}".format(api_key_index, new_api_key_index))
            else:
                new_api_key_index = 0
                print_line("API limit reached for all API keys, sleeping for 1 hour")
                time.sleep(3600)
            
            # Update API key
            api_key_index = new_api_key_index
            continue

        print("Progress: Extracted {} for the time period {} to {}".format(company, extract_start_date, extract_end_date))

        # Save query results progressively
        with open(output_path, 'a', newline='') as f:
            writer = csv.writer(f)

            for article in response_text['articles']:
                title = preprocess_text(article["title"]).encode('utf-8').decode('utf-8')
                date = datetime.strptime(article["published"], '%a, %d %b %Y %H:%M:%S %Z')
                date_posted = date.strftime('%Y-%m-%d')
                year = date.isocalendar()[0] # Extracting year
                week = date.isocalendar()[1] # Extracting week
                writer.writerow([company, title, date_posted, year, week])

        # Update extract start date to obtain next week data
        extract_start_date = extract_end_date
        

if __name__ == "__main__":
    # Set date parameters (year, month, day)
    start_date = date(config.START_DATE[0], config.START_DATE[1], config.START_DATE[2])
    end_date = date(config.END_DATE[0], config.END_DATE[1], config.END_DATE[2])
    print("Start date: " + start_date.strftime('%Y-%m-%d'))
    print("End date: " + end_date.strftime('%Y-%m-%d'))
    today = date.today()

    # Obtain API keys
    api_keys = config.API_KEYS
    print("{} API keys received".format(len(api_keys)))

    # Set path
    companies_path = 'companies.txt'
    output_path = 'data/initialise_news {}.csv'.format(today)

    # Write header for output file
    col_names = ['company_name', 'title', 'date_posted', 'year', 'week'] # 'score'
    
    # Create new file with headers if file does not exist
    if not os.path.isfile(output_path):
        print("Creating new file for storage at {}".format(output_path))
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(col_names)    
    else:
        print("Storing in existing file {}".format(output_path))

    # Load companies for extraction
    companies = open(companies_path).read().split()
    
    # Extract news for all companies
    for company in companies:
        print_banner("Extracting news: " + company)
        extract_news(company)
