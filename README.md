# Sentiment Analysis of Companies using Financial News 

This project aims to create an interactive dashboard/application which displays Sentiment Analysis scores of Companies using the most recent financial news.

## Getting Started
To collect the financial news data, we will be using [Google News API from RapidAPI](https://rapidapi.com/newscatcher-api-newscatcher-api-default/api/google-news/).
Register and get your API key ready for the following steps.

### Project Directory Structure
```
├── models
│   ├── classifier_model
│   │   ├── finbert-sentiment
│   │   │   ├── config.json
│   │   │   ├── pytorch_model.bin
│   │   │   ├── pytorch_model.bin.cpgz
├── news_data
│   ├── amazon_titles.json
│   ├── amazon_titles.csv
│   ├── ...
├── score_data
│   ├── amazon_score.csv
│   ├── ...
├── GnewsAPI_amazon.py
├── predict.py
├── environment.yml
.   .
.   .
```

## Data Collection of Financial News
To collect the financial news using Google News API, insert your API key into the `GnewsAPI_amazon.py` file and run.

(Note: To scale up and make this process more modular so that we can run the code for multiple companies at once, 
also to terminate program once there are no more available news)

```
$ python GnewsAPI_amazon.py
```

(Note: To be edited, output files to be stored in `news_data/` folder, edit code to allow easy manipulation of parameters such as time frame)
As the Google News API has a query limit of 5 requests per hour, the code has been adjusted to work around that limitation.
As of now, we have collected weekly news titles for 2020 for Amazon, Apple and Netflix, with the start of week on Mondays.

## Applying FinBERT Sentiment Analysis Model
We will be using [FinBERT](https://github.com/ProsusAI/finBERT) to transform news titles into sentiment scores. 

### Downloading Pre-trained Model
Retraining of the FinBERT model is possible if needed. However for our case, we are using the pretrained sentiment 
analysis model trained on Financial PhraseBank data which can be downloaded from
[here](https://prosus-public.s3-eu-west-1.amazonaws.com/finbert/finbert-sentiment/pytorch_model.bin).

For this model, the workflow should be like this:
* Download the model and put it into the directory `models/classifier_model/finbert-sentiment/`.
* Call the model with `.from_pretrained(<model directory name>)`

### Installation
Install the dependencies by creating the Conda environment `finbert` from the given `environment.yml` file and activating it.
(Note: To double check for any other dependencies that should be listed out)


```
conda install -c pytorch pytorch
pip install pytorch-pretrained-bert
conda install nltk
conda env create -f environment.yml
conda activate finbert
```

Start your python terminal in command prompt by entering `python` or `python3` and run the following code:
```
import nltk
nltk.download('punkt')
```

### Getting Predictions
Given a .csv file, `predict.py` produces a .csv file including the sentences in the text, corresponding softmax probabilities for three labels, actual prediction and sentiment score (which is calculated with: probability of positive - probability of negative).

```
python predict.py --text_path news_data/COMPANYNAME_titles.csv --output_dir score_data/ --model_path models/classifier_model/finbert-sentiment
```

## Web Application with Visualisations