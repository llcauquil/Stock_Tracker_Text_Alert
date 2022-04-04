##  an alert system that uses stock and twilio api to alert of changes in a desired stock (TESLA), then text an alert of a percent change,
#  followed by the next three headlines concerning the stock.
# You will need an alphavantage account, twilio account, and a newsapi account to run this process, inserting needed api keys where you need
# UPDATES FROM PREVIOUS DAY

import requests
from twilio.rest import Client # you will need a twilio account to work the client

#-----------------------------------------Params

# NOTE: You will need api keys for twilio, newsapi and alphavantage, please insert below. You are also going to need to input the needed phone numbers 
STOCK_API_KEY = ""
NEWS_API = ""

TWILIO_ACCOUNT_SID = ""
TWILIO_TOKEN = ""

SENDING_NUMBER = "" #the free phone number givin to you by Twilio
RECIEVING_NUMBER = ""

# api endpoints to receieve needed information
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# NOTE: change the STOCK_NAME to allow for different searches
STOCK_NAME = ""
COMPANY_NAME = ""

stock_param = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

#-----------------------------------------Processing the data collected from API's

# Stock API request - getting yesterday's stock closing price
response = requests.get(STOCK_ENDPOINT, params=stock_param )
data = response.json()["Time Series (Daily)"]
#data_list = [new_item for item in list] - convention for python priority list making
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

# getting the day before yesetrday's closing data for comparising
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))

perc_diff = difference/float(yesterday_closing_price) *100 # calculating the percentage diff

#-----------------------------------------Using the data to get the news articles and sending out the text message

# getting the related news articles if triggered
if(perc_diff > 3): #checks if the percent change for the last two days is greater than 3%
    news_param = { # json param
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API
    }
    news = requests.get(NEWS_ENDPOINT, params = news_param)
    articles = news.json()["articles"]
    three_article = articles[:3]

formatted_message = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_article]

client = Client (TWILIO_ACCOUNT_SID,TWILIO_TOKEN) # setting the texting object to then send the news articles

# sending the text message
for article in formatted_message:
    message = client.messages.create(
        body = article,
        from_= SENDING_NUMBER,
        to= RECIEVING_NUMBER
    )
