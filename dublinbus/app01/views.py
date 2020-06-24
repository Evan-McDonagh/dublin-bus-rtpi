import json

<<<<<<< HEAD
<<<<<<< Updated upstream
from django.contrib.sites import requests
from django.shortcuts import render,HttpResponse
=======
#  Google Map Apikey
gmap_api = 'AIzaSyB_Bqco2DvRVp55QdFyANIiDRSKS8IE8p8'

#  OpenWeather Forecast Apikey
weather_fore_api = '9570260da25526e20bf66bdf7e1c25e5'

# OpenWeather Preent Apikey
weather_pre_api = 'c9d5929c3180f174f633828540c0fbc5'
import requests
from django.http import HttpResponse
from django.shortcuts import render
from pyleapcard import *
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
    return render(request, 'home.html')
=======
    return render(request, 'home.html', context)
>>>>>>> Stashed changes

=======
from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render
from pyleapcard import *

from .forms import leapForm


# Create your views here.
def home(request):
    context = load_bus_data()
    # get LAT, LNG from front-end
    return render(request, 'home.html',context)
>>>>>>> dev
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
<<<<<<< HEAD
    return HttpResponse(json.dumps(inifo))
=======
    return HttpResponse(json.dumps(inifo))

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
    return render(request,'leapcard.html', {'form' : form})
>>>>>>> dev
