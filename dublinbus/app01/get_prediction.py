import pandas as pd
import numpy as np
import pickle
import datetime
import os

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_score
from sklearn.tree import export_graphviz
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR


import warnings


def get_prediction(route,direction,datestring,stopA,stopB):
    """
        Scrapes weather data and returns a prediction for the given inputs.
    """
    datetime_departure = datetime.datetime.strptime(datestring,'%Y-%m-%d %H:%M:%S')

    forecast = find_forecast(datetime_departure)        
    
    prediction = predict_travel_time(route,direction,datetime_departure,forecast['feels_like'],forecast['weather_main'],stopA,stopB)
    
    return int(prediction)

def find_forecast(datetime_departure):
    """
        Returns 5 day weather forecast if one is available prior to the given datetime.
        Otherwise returns average weather conditions for the month of the given datetime.
    """
    forecast = get_5day_forcast()
    for i,f in enumerate(forecast['list']):
        if datetime.datetime.fromtimestamp(f['dt']) > datetime_departure:
            f_out = {'feels_like':f['main']['feels_like']-273.15,'weather_main':f['weather'][0]['main']}
            return f_out

    filepath = os.path.join(os.path.dirname(__file__), 'models_SVR/avg_monthly_weather.pkl')
    avg_monthly_weather = pickle.load(open(filepath,'rb'))

    f_out = {
        'feels_like':avg_monthly_weather['feels_like'].iloc[datetime_departure.month],
        'weather_main':avg_monthly_weather['weather_main'].iloc[datetime_departure.month]
    }
    return f_out
    
def predict_travel_time(route,direction,datetime_departure,feels_like,weather_main,stopA,stopB):
    """
        Determines the first trip of the day that will reach  stopA and determines the travel time between stopA and stopB based on the statistical fraction of the total predicted travel time.
    """
    filepath_departures = os.path.join(os.path.dirname(__file__), 'models_SVR/departure_times.pkl')
    filepath_stopfractions = os.path.join(os.path.dirname(__file__), 'models_SVR/stopfractions.pkl')

    departure_times = pickle.load(open(filepath_departures,'rb'))
    stopfractions = pickle.load(open(filepath_stopfractions,'rb'))
    
    stopA_frac = stopfractions[stopfractions['LINEID']==route][stopfractions['DIRECTION']==direction][stopfractions['STOPPOINTID']==stopA]['TRIP_FRAC'].iloc[0]
    stopB_frac = stopfractions[stopfractions['LINEID']==route][stopfractions['DIRECTION']==direction][stopfractions['STOPPOINTID']==stopB]['TRIP_FRAC'].iloc[0]
    fraction = stopB_frac - stopA_frac
    
    schedule = [datetime_departure.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(seconds=int(t)) for t in departure_times[route][direction][datetime_departure.weekday()]]

    predictions = predict_total_triptimes(route,direction,schedule,feels_like,weather_main)
    for i, start_time in enumerate(schedule):
        if start_time + datetime.timedelta(seconds=predictions[i]*stopA_frac) > datetime_departure:
            prediction = predictions[i]*fraction
            return prediction


def predict_total_triptimes(route,direction,datetimes_departure,feels_like,weather_main):
    """
        Predicts end-end traveltimes for a give nroute and direction for a litst of provided departure datetimes under given weather conditions.
        Returns a a series of predictions.
    """

    model = find_model(route,direction)
    
    feels_like = normalize(feels_like,model['max_feels_like'],model['min_feels_like'])
    
    params = {feature:[0]*len(datetimes_departure) for feature in model['columns']}
    
    for i, dt in enumerate(datetimes_departure):
        time_in_seconds = dt.hour*60*60 + dt.minute*60 + dt.second
        plannedtime_dep_cos = np.cos(2*np.pi*time_in_seconds/(60*60*24))
        plannedtime_dep_sin = np.sin(2*np.pi*time_in_seconds/(60*60*24))
        month = dt.month
        weekday = dt.weekday()
        weekend = True if weekday in [5,6] else False
        rush_hour = (25200 < time_in_seconds < 32400) or (57600 < time_in_seconds < 68400)
    
        params['RUSH_HOUR_' + str(rush_hour)][i] = 1
        params['PLANNEDTIME_DEP_COS'][i] = plannedtime_dep_cos
        params['PLANNEDTIME_DEP_SIN'][i] = plannedtime_dep_sin
        params['feels_like'][i] = 1
        params['MONTH_' + str(month)][i] = 1
        params['WEEKDAY_' + str(weekday)][i] = 1
        params['WEEKEND_' + str(weekend)][i] = 1
        params['weather_main_' + str(weather_main)][i] = 1
    
    d = pd.DataFrame(params,index=[i for i in range(len(datetimes_departure))],columns=model['columns'])
    
    predictions = unnormalize(model['model'].predict(d), model['max_trip'], model['min_trip'])
    
    return predictions

def unnormalize(x_norm,x_max,x_min):
    """Returns a non-normalised value given a normalised value and the known maximum and minimum"""
    return x_norm*(x_max - x_min) + x_min

def normalize(x,x_max,x_min):
    """Normalised a value given a maximum and a minimum"""
    return (x - x_min)/(x_max - x_min)

def find_model(route,direction):
    """Searches the models file for the model with a matching route and direction of travel"""
    
    filepath = os.path.join(os.path.dirname(__file__), "models_SVR/models.pkl")
    models = pickle.load(open(filepath, "rb"))
    for model in models:
        if model['route'] == route and model['direction'] == direction:
            return model

def get_5day_forcast():
    """Scrapes weather data from openweathermap.org"""

    import requests
    
    API_KEY = "16fb93e92d3bd8aefd9b647c1a8f6acf"
    URL = "http://api.openweathermap.org/data/2.5/forecast?q=Dublin,ie&appid=" + API_KEY
    
    try:
        r = requests.get(url = URL)
    except: 
        print("Scraping error: data not collected.")
        return None
    
    weather = r.json()
    return weather