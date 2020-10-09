from finbert.finbert import predict
from pytorch_pretrained_bert.modeling import BertForSequenceClassification
import argparse
from pathlib import Path
import datetime
import os
import random
import string
import csv


parser = argparse.ArgumentParser(description='Sentiment analyzer')

parser.add_argument('-a', action="store_true", default=False)

parser.add_argument('--text_path', type=str, help='Path to the text file.')
parser.add_argument('--output_dir', type=str, help='Where to write the results')
parser.add_argument('--model_path', type=str, help='Path to classifier model')

args = parser.parse_args()

if not os.path.exists(args.output_dir):
    os.mkdir(args.output_dir)


model = BertForSequenceClassification.from_pretrained(args.model_path,num_labels=3,cache_dir=None)
#now = datetime.datetime.now().strftime("predictions_%B-%d-%Y-%I:%M.csv")
# random_filename = ''.join(random.choice(string.ascii_letters) for i in range(10))
output = 'results.csv'
# create csv file
output_path=os.path.join(args.output_dir,output)
with open(output_path, 'w') as f:
    fieldnames = ['Review', 'Date', 'Year', 'Week', 'logit', 'prediction', 'sentiment_score']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
f.close()


with open(args.text_path,'r') as f:
    reader = csv.reader(f)
    next(reader, None)  # skip the header
    for row in reader:
        # row = Date, Review, Week, Year
        date=row[0]
        text = row[1] # Review
        week = row[2]
        year = row[3]
        predict(text,model, date, year, week, write_to_csv=True,path=os.path.join(args.output_dir,output))
