# Sentiment Analysis of Companies using News Titles

This project aims to create an interactive dashboard which displays Sentiment Analysis scores of Companies using the most recent news. This repository contains the steps to obtain data and sentiment scores, the web application codes can be accessed on the [DevOps_Fintech_Website](https://github.com/NUS-Fintech-Society/DevOps_Fintech_Website) and [DevOps_Fintech_Website_Backend](https://github.com/NUS-Fintech-Society/DevOps_Fintech_Website_Backend) repository.

## Project Directory Structure
```
├── data
│   ├── initialise_news XXXX-XX-XX
├── initialise_news.py
├── predict.py
.   .
.   .
```

## Data Collection of Financial News
Currently, data is populated for [Top 30 companies on NASDAQ Index](https://disfold.com/top-companies-us-nasdaq/) (as of 2020) for the time period 2020 Jan to 2021 Feb. The companies are saved in `companies.txt` and are used for news querying on [Google News API on RapidAPI](https://rapidapi.com/newscatcher-api-newscatcher-api-default/api/google-news/).

As the Google News API has a query limit of 3 requests per hour, code has been adjusted to work around that limitation and loop around multiple API keys to fetch news in a more efficient manner. Data shall be fetched and stored into csv, then subsequently processed for prediction score and populated into the SQLite3 database used for the Fintech Society website.

### Adding New Companies
To add in new companies, run `python initialise_news.py`. Data obtained will be stored in a csv file.

### Adding New Time Period
To add in news for new time period, run `python update_news.py`.


Note: run predict and updating to database to be updated
## Getting Predictions
Given a .csv file, `predict.py` produces a .csv file including the sentences in the text.