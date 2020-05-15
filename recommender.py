from flask import Flask
from pprint import pprint
import requests
from datetime import *
import json
from pymongo import MongoClient
app = Flask(__name__)

# MongoDB connexion
client = MongoClient('localhost', 27017)
db = client.prueba

def get_temperature():
    # Gets clime from http://api.openweathermap.org/data/
    r = requests.get()
    open_weather_response = r.json()
    temperature = open_weather_response['main']['temp']
    temp_max = open_weather_response['main']['temp_max']
    temp_min = open_weather_response['main']['temp_min']
    humidity = open_weather_response['main']['humidity']
    clime = open_weather_response['weather'][0]['main']
    # Default
    rsp = 'normal'

    if temperature > 33:
        rsp = 'hot'
    elif temperature < 12:
        rsp = 'cold'
    return rsp


def get_station():
    # Here we have the station dates from Paraguay
    present = datetime.now().date()
    summer = datetime.strptime('12/21/18', "%m/%d/%y").date()
    autumn = datetime.strptime('3/21/18', "%m/%d/%y").date()
    winter = datetime.strptime('6/21/17', "%m/%d/%y").date()
    spring = datetime.strptime('9/21/17', "%m/%d/%y").date()
    station = ''
    if (present > summer and present < autumn):
        station = 'summer'
    if (present > autumn and present < winter):
        station = 'autumn'
    if (present > winter and present < spring):
        station = 'winter'
    if (present > spring and present < summer):
        station = 'spring'
    return station

def get_relevant_dates():
    summer_begins = datetime.strptime('12/21/18', "%m/%d/%y").date()
    return summer_begins

def get_recommendations(clime, station):
    clime = 'hot'
    recommendation = []
    recommendation_set = {}
    recommendation_set['station'] = {}
    recommendation_set['clime'] = {}

    recommendation_set['station']['winter'] = [
        {'ranking': "1", 'product': "p1"},
        {'ranking': "2", 'product': "p2"},
        {'ranking': "3", 'product': "p3"},
        {'ranking': "4", 'product': "p4"},
        {'ranking': "5", 'product': "p5"},
        {'ranking': "6", 'product': "p6"},
        {'ranking': "7", 'product': "p7"},
        {'ranking': "8", 'product': "p8"},
        {'ranking': "9", 'product': "p9"},
        {'ranking': "10", 'product': "p10"},
    ]
    recommendation_set['clime']['calor'] = [
        {'ranking': "1", 'product': "p1"},
        {'ranking': "2", 'product': "p2"},
        {'ranking': "3", 'product': "p3"},
        {'ranking': "4", 'product': "p4"},
        {'ranking': "5", 'product': "p5"},
        {'ranking': "5", 'product': "p5"},
        {'ranking': "5", 'product': "p5"},
        {'ranking': "5", 'product': "p5"},
        {'ranking': "5", 'product': "p5"},
        {'ranking': "5", 'product': "p5"},
    ]

    recommendation.append(recommendation_set['clime'][clime])
    recommendation.append(recommendation_set['station'][station])
    return recommendation


def get_expert_recommendation():
    recommendation = []
    recommendation_set = [
        {'ranking': "1", 'product': "p1"},
        {'ranking': "2", 'product': "p2"},
        {'ranking': "3", 'product': "p3"},
        {'ranking': "4", 'product': "p4"},
        {'ranking': "5", 'product': "p5"},
        {'ranking': "6", 'product': "p6"},
        {'ranking': "7", 'product': "p7"},
        {'ranking': "8", 'product': "p8"},
        {'ranking': "9", 'product': "p9"},
        {'ranking': "10", 'product': "p10"},
    ]
    recommendation.append(recommendation_set)
    return recommendation


def get_company_recommendation():
    # recommendation_set = {}
    recommendation = []
    recommendation_set = [
        {'ranking': "1", 'product': "p1"},
        {'ranking': "2", 'product': "p2"},
        {'ranking': "3", 'product': "p3"},
        {'ranking': "4", 'product': "p4"},
        {'ranking': "5", 'product': "p5"},
        {'ranking': "6", 'product': "p6"},
        {'ranking': "7", 'product': "p7"},
        {'ranking': "8", 'product': "p8"},
        {'ranking': "9", 'product': "p9"},
        {'ranking': "10", 'product': "p10"},
    ]

    recommendation.append(recommendation_set)
    return recommendation


def optimize_recommendation():
    pass

@app.route('/')
def get_event_recommendation():
    # Recommends products by clime
    clime = get_temperature()
    # Recommends products by station
    station = get_station()
    # Recommends products by a relevant date
    relevat_date = get_relevant_dates()
    recommendations = get_recommendations(clime, station)
    print(recommendations)
    result = db.recommendation.insert_one(
         {"clime":recommendations[0]}
    )
    print(result.inserted_id)
    return "Test"


@app.route('/train')
def entrenar():
    expert = get_expert_recommendation()
    company = get_company_recommendation()
    event = get_event_recommendation()

    #TODO Read data and insert into the multiobjective optimization method.
    recommendation = optimize_recommendation()

    return 'training model'

if __name__ == '__main__':
    app.run()
