import json

from django.contrib.sites import requests
from django.shortcuts import render,HttpResponse

#  Google Map Apikey
gmap_api = 'AIzaSyB_Bqco2DvRVp55QdFyANIiDRSKS8IE8p8'

#  OpenWeather Forecast Apikey
weather_fore_api = '9570260da25526e20bf66bdf7e1c25e5'

# OpenWeather Preent Apikey
weather_pre_api = 'c9d5929c3180f174f633828540c0fbc5'


# To initialize the home page of this project.
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def index(request):
    context = load_bus_data()
    return render(request,'index.html', context)

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
def home(request):
    # get LAT, LNG from front-end
    return render(request, 'home.html')

def init(request):
    print(request.method)
    inifo = {}
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
        descp = str(weather_result["weather"][0].get('main'))    # get weather description

        weather = descp + ', ' + temp
        inifo['weather'] = weather
        print(weather)
        # # get the address of the post coordinate
        address_request = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key={}'.format(lat, lng, gmap_api))
        address_result = json.loads(address_request.text)
        print(address_result)
        address = address_result['results'][0].get('formatted_address')
        print(address)
        inifo['address'] = address
        print(inifo)
    return HttpResponse(json.dumps(inifo))