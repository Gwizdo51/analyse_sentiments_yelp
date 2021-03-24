from time import time, sleep
from transformers import CamembertTokenizer, TFAutoModelForSequenceClassification
from fastapi import FastAPI  # Calling the FastAPI library
import pandas as pd

# import necessary files
import scrapper
import sentiment_analysis
import json_maker

# load the model and tokenizer for sentiment analysis
tokenizer = CamembertTokenizer.from_pretrained("camembert-base")
model = TFAutoModelForSequenceClassification.from_pretrained("tblard/tf-allocine")

# Declaring as the main app to use FastAPI
app = FastAPI()

# url : http://127.0.0.1:8000
# interactive interface : http://127.0.0.1:8000/docs
# command line : uvicorn API:app --reload

@app.get("/")
def root(activity_field: str = None, location: str = None):

    if activity_field == None or location == None:
        result = []
    else:
        # scrap the data and store it in dataframes
        df_businesses, df_reviews = scrapper.scrapper(activity_field, location)

        # analyse the reviews stored in df_reviews
        df_reviews = sentiment_analysis.analyse_reviews(df_reviews, tokenizer, model)

        # create a dictionary that will hold the information the API will send as JSON
        result = json_maker.json_maker(activity_field, location, df_businesses, df_reviews)
    
    return result

# How to use :
# http://localhost:8000/?activity_field=Restaurants&location=Reims