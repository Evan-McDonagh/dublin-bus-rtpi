import re

from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from app01 import models
from .forms import leapForm,routeForm
from pyleapcard import *
from pprint import pprint
import json
import requests

#  Google Map Apikey
gmap_api = 'AIzaSyB_Bqco2DvRVp55QdFyANIiDRSKS8IE8p8'

#  OpenWeather Forecast Apikey
weather_fore_api = '9570260da25526e20bf66bdf7e1c25e5'

# OpenWeather Preent Apikey
weather_pre_api = 'c9d5929c3180f174f633828540c0fbc5'


def base(request):
    context = load_bus_data()
    return render(request,'base.html', context=context)


def search(request):
    context = load_bus_data()
    context['title'] = 'search'
    return render(request, 'search.html', context)

def load_bus_data():
    #load bus stop and route data
    import json
    import os
    dirname = os.path.dirname(__file__)
    stopfile = os.path.join(dirname, "../local-bus-data/stop-data.json")
    routefile = os.path.join(dirname, "../local-bus-data/route-data.json")
    with open(stopfile) as infile:
        stop_data = json.load(infile)
    with open(routefile) as infile:
        route_data = json.load(infile)
    stopdump = json.dumps(stop_data)
    context = {'stopdata':stopdump}
    return context

# load_bus_data()
def leapcard(request):

    if request.method == 'POST':
        form = leapForm(request.POST)
        # print(form)
        if form.is_valid():
            name = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            context = {}
            # print(name,pwd)
            try:
                session = LeapSession()
                session.try_login(name,pwd)
                overview = session.get_card_overview()
                # print(overview)
                leap_content = vars(overview)
                context['card_num'] = leap_content.get('card_num')
                context['balance'] = leap_content.get('balance')
                # context['leap_content'] = leap_content


            except:
                context['wrong'] = "The user or the password is wrong, please try again"
                print("the wrong password")
            finally:
                context['form'] = form
                return render(request,'leapcard.html', context = context)



    form = leapForm()
    return render(request,'leapcard.html', {'form': form, 'title': 'Leapcard'})


def stop(request):
    if request.method == 'POST':
        form = routeForm(request.POST)
        if form.is_valid():
            stop_id = form.cleaned_data['stop_id']


            url = "https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation" +"?stopid=" + stop_id+"&format=json"
            obj = requests.get(url)
            obj_json = obj.json()
            # print(obj_json)

            context = {}
            results = obj_json['results']
            context['results'] = results
            context['form'] = form
            context['length'] = len(results)
            stop_data = load_bus_data()
            context['stopdata'] = stop_data['stopdata']
            # context = load_bus_data()
            # print(context )


            return render(request,"stop.html", context=context)
    
    context = {}
    stop_data = load_bus_data()
    form = routeForm()
    context = {
        'stopdata' : stop_data['stopdata'],
        'form':form,
    }
    context['title'] = 'stop'
    return render(request,'stop.html',context=context) 

def init(request):
    print(request.method)
    inifo = {}
    if request.method == 'POST':
        print(request.body)
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        print(lat, lng)


        # # get present weather
        # weather_r = requests.get(
        #     "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(lat, lng, weather_pre_api))
        # weather_result = json.loads(weather_r.text)
        # print(weather_result)
        # h_temp = weather_result["main"].get("feels_like")  # get tempetature
        # temp = str(round(h_temp - 273.15)) + '˚C'
        # descp = str(weather_result["weather"][0].get('main'))    # get weather description
        #
        # weather = descp + ', ' + temp
        # inifo['weather'] = weather
        print(weather)
        # # get the address of the post coordinate
        address_request = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key={}'.format(lat, lng, gmap_api))
        address_result = json.loads(address_request.text)
        print(address_result)
        address = address_result['results'][0].get('formatted_address')
        print(address)
        inifo['address'] = address
        print(inifo)
    else:
        inifo['address'] = 'location unknown'
    return HttpResponse(json.dumps(inifo))

def weather(request):
    print('weather')
    weather_info = {}
    if request.method == 'POST':
        print(request.body)
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        print(lat, lng)

        # get present weather
        weather_r = requests.get(
            "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(lat, lng, weather_pre_api))
        weather_result = json.loads(weather_r.text)
        print(weather_result)
        h_temp = weather_result["main"].get("feels_like")  # get tempetature
        temp = str(round(h_temp - 273.15)) + '˚C'
        descp = str(weather_result["weather"][0].get('main'))  # get weather description

        weather = descp + ', ' + temp
        weather_info['weather'] = weather
        print(weather_info)
    else:
        weather_info['weather'] = 'location unknown'
    return HttpResponse(json.dumps(weather_info))


def real_info(request):
    if request.method == 'POST':
        form = routeForm(request.POST)
        # print(request.body)
        a = str(request.body)
        b = re.search("stop[^']*", a).group()
        c = b.split("D")[-1]

        # url = "https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid=3562&format=json"
        url = "https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation" + "?stopid=" + c + "&format=json"
        obj = requests.get(url)
        obj_json = obj.json()

        return JsonResponse(obj_json, safe=False)

def twitter(request):
    return render(request,'twitter.html')