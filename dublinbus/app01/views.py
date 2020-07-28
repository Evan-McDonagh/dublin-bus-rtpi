import math
import re

from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from app01 import models
from .forms import leapForm,routeForm
from pyleapcard import *
from pprint import pprint
import json
import requests
import re
import os

#  Google Map Apikey
gmap_api = 'AIzaSyB_Bqco2DvRVp55QdFyANIiDRSKS8IE8p8'

#  OpenWeather Forecast Apikey
weather_fore_api = '9570260da25526e20bf66bdf7e1c25e5'

# OpenWeather Preent Apikey
weather_pre_api = 'c9d5929c3180f174f633828540c0fbc5'

dirname = os.path.dirname(__file__)
stopfile = os.path.join(dirname, "../local-bus-data/stop-data.json")
routefile = os.path.join(dirname, "../local-bus-data/all-routes-sequences.json")

with open(routefile) as rt:
    allroutes = json.load(rt)
    rt.close()
with open(stopfile) as st:
    allstops = json.load(st)
    st.close()

# Create your views here.
def index(request):
    
    context = load_bus_data()
    return render(request,'index.html', context)

def load_bus_data():
    #load bus stop and route data
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


def leapcard(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        context = {}
        
        try:
            session = LeapSession()
            session.try_login(username,password)
            overview = session.get_card_overview()
            # print(overview)
            leap_content = vars(overview)
            context['card_num'] = leap_content.get('card_num')
            context['balance'] = leap_content.get('balance')

        except:
            context['wrong'] = "The user or the password is wrong, please try again"
            print("the wrong password")
            return JsonResponse(context,safe=False)
        
        return JsonResponse(context,safe=False)

def stop(request):
    if request.method == 'POST':
        stop_id = request.POST['stop_id']
        url = "https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation" +"?stopid=" + stop_id+"&format=json"
        obj = requests.get(url)
        obj_json = obj.json()
        print(obj_json)
        return JsonResponse(obj_json, safe=False)

# get user address info by user's location
def init(request):
    inifo = {}
    if request.method == 'POST':
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')

        # get the address of the post coordinate
        address_request = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key={}'.format(lat, lng, gmap_api))
        address_result = json.loads(address_request.text)
        address = address_result['results'][0].get('formatted_address')
        inifo['address'] = address
    else:
        inifo['address'] = 'location unknown'
    return HttpResponse(json.dumps(inifo))
    

# get realtime weather at the users' location
def weather(request):
    weather_info = {}
    if request.method == 'POST':
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')

        # get present weather
        weather_r = requests.get(
            "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(lat, lng, weather_pre_api))
        weather_result = json.loads(weather_r.text)
        h_temp = weather_result["main"].get("feels_like")  # get temperature
        temp = str(round(h_temp - 273.15)) + '˚C'
        descp = str(weather_result["weather"][0].get('main'))  # get weather description

        # get the relative icon
        weather_icon = weather_result["weather"][0].get("icon")
        iconUrl = "http://openweathermap.org/img/wn/" + weather_icon + ".png"

        weather_info['descp'] = descp
        weather_info['temp'] = temp
        weather_info['iconUrl'] = iconUrl

    else:
        weather_info['weather'] = 'location unknown'
    return HttpResponse(json.dumps(weather_info))


# select involved stops along the route.
def printresult(request):
    if request.method == 'POST':
        segments = json.loads(request.body)
        seg_stops = {}
        for seg in segments:
            busname = seg['busname']
            alongroutestops = matchstop(seg, allstops)
            print(len(alongroutestops), alongroutestops)
            alongroutestopinfos = []
            # print(alongroutestops)
            for stop in alongroutestops:
                for stopkey in allstops:
                    if stop == stopkey:
                        STOP = allstops[stopkey]
                        alongroutestopinfos.append({"id":STOP['stopno'], 'lat':STOP["latitude"], 'lng':STOP["longitude"]})
            seg_stops[busname] = alongroutestopinfos
        # print(seg_stops)
        return JsonResponse(seg_stops, safe=False)


def matchstop(seg, allstops):
    busname = seg['busname']
    startstopname = seg['startstopname']
    startstoplocation = seg['startstoplocation']
    endstopname = seg['endstopname']
    endstoplocation = seg['endstoplocation']
    headsign = seg['headsign']
    numstops = seg['numstops']
    pattern = re.compile(r'(?<=stop )\d+\.?\d*')
    alongroutestopids = []
    print('start',startstopname, pattern.findall(startstopname))
    print('stop',endstopname, pattern.findall(endstopname))
    if len(pattern.findall(startstopname)) > 0 and len(pattern.findall(endstopname)) > 0:
        startstopno = pattern.findall(startstopname)[0]
        endstopno = pattern.findall(endstopname)[0]
        startstopkey = ""
        endstopkey = ""
        for stopkey in allstops:
            if allstops[stopkey].get('stopno') == startstopno:
                startstopkey = stopkey
                continue
            if allstops[stopkey].get('stopno') == endstopno:
                endstopkey = stopkey
                continue
        for route in allroutes:
            if route == busname:
                ROUTE = allroutes[route]
                for in_out in ROUTE:
                    atcocodes = ROUTE[in_out]['atcocodes']
                    # print(atcocodes)
                    if startstopkey in atcocodes and endstopkey in atcocodes:
                        startindex = atcocodes.index(startstopkey)
                        endindex = atcocodes.index(endstopkey)
                        if startindex <= endindex:
                            alongroutestopids = atcocodes[startindex:endindex + 1]
                            return alongroutestopids
                        else:
                            alongroutestopids = atcocodes[endindex:startindex + 1]
                            return  alongroutestopids
                    else:
                        continue
    elif len(pattern.findall(startstopname)) > 0:
        startstopno = pattern.findall(startstopname)[0]  # if startstopname contains stopno info
        for stopkey in allstops:
            if allstops[stopkey].get('stopno') == startstopno:
                alongroutestopids += slicealongroutestopsid(stopkey, busname, numstops, "start")
                # print('startno', alongroutestopids)
                return alongroutestopids
    elif len(pattern.findall(endstopname)) > 0:
        endstopno = pattern.findall(endstopname)[0]
        for stopkey in allstops:
            if allstops[stopkey].get('stopno') == endstopno:
                print(stopkey)
                alongroutestopids += slicealongroutestopsid(stopkey, busname, numstops, "end")
                # print('stopno', alongroutestopids)
                return alongroutestopids
    else:
        distance = 0.01
        longstopid = ""
        routestopskeys = allroutes[busname]['Inbound']['atcocodes'] + allroutes[busname]['Outbound']['atcocodes']
        print(routestopskeys)
        routestops = {}
        for stopkey in allstops:
            for key in routestopskeys:
                if stopkey == key:
                    routestops[stopkey] = allstops[stopkey]
        print(routestops)
        for stopkey in routestops:
            if routestops[stopkey].get('latitude') is not None:
                stop_loc = {'lat': routestops[stopkey].get('latitude'), 'lng': routestops[stopkey].get('longitude')}
            else:
                print(stopkey, "location does not exist, replaced with {0,0}")
                stop_loc = {'lat': 0, 'lng': 0}
            DIST = gettwostopdistance(startstoplocation, stop_loc);
            if DIST >= distance:
                continue
            else:
                distance = DIST
                longstopid = stopkey
        alongroutestopids += slicealongroutestopsid(longstopid, busname, numstops, "start")
        print('startloc', alongroutestopids)
        return alongroutestopids


def gettwostopdistance(loc1, loc2):
    # print('loc1',loc1)
    # print('loc2',loc2)
    # print('comparing locations')
    lat_diff = loc1['lat'] - loc2['lat']
    lng_diff = loc1['lng'] - loc2['lng']
    dist = math.sqrt(pow(lat_diff, 2)+pow(lng_diff, 2))
    return dist


def slicealongroutestopsid(longstopid, busname, numstops, start_or_end):
    print("numstops", numstops)
    for route in allroutes:
        if route == busname:
            ROUTE = allroutes[route]
            for in_out in ROUTE:
                atcocodes = ROUTE[in_out]['atcocodes']
                for i in range(0, len(atcocodes)):
                    if atcocodes[i] == longstopid:
                        print('i', i)
                        if start_or_end == 'start':
                            if i+numstops+1 <= len(atcocodes):
                                alongroutestopids = atcocodes[i:i+numstops+1]
                                return alongroutestopids
                            else:
                                continue
                        else:
                            if i-numstops >= 0:
                                alongroutestopids = atcocodes[i-numstops:i+1]
                                return alongroutestopids
                            else:
                                continue

# show realtime info when a marker alongside the route is clicked
def rtmarkerinfo(request):
    if request.method == 'POST':
        stop_id = request.POST.get('id')
        url = "https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation" +"?stopid=" + stop_id+"&format=json"
        obj = requests.get(url)
        obj_json = obj.json()
        # print(stop_id)
        allinfo = "Stop No." + obj_json.get('stopid') +"<br>"
        rsp ={obj_json.get('stopid'): []}
        for result in obj_json['results']:
            key = result.get('route')
            rsp[obj_json.get('stopid')].append({key: {'arrivaltime':result.get('arrivaldatetime'), 'destination':result.get('destination')}})
            allinfo += "Route:"+ key + "  arrive at:" + result.get('arrivaldatetime') + " Towards " + result.get('destination') +"<br>"
        return HttpResponse(json.dumps({"allinfo":allinfo}))

# show prediction
def showprediction(request):
    #  just pring some info, but later on, the pkl file can be added and give prediction using info contained in segs.
    # if request.method == 'POST':
    #     segs = json.loads(request.body)
    #     for seg in segs:
    #         for key in seg:
    #             print(key, ":", seg[key])
    #         print('----------------')
    return HttpResponse(json.dumps({'prediction': "prediction info"}))

