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
    # if request.method == 'POST':
    #     rebody = json.loads(request.body)
    #     # with open ('result.txt', 'w') as rt:
    #     #     rt.write(str(rebody))
    #     # rt.close()
    #     bounds = rebody.get('bounds')
    #     bus = rebody.get('bus')
    #     with open("./local-bus-data/route-data.json") as rt:
    #         allroutes = json.load(rt)
    #         rt.close()
    #     with open("./local-bus-data/stop-data.json") as st:
    #         allstops = json.load(st)
    #         st.close()
    #     stop_locations = []
    #
    #     # route_stop_locations = {}
    #     for i in bus:
    #         bus_route = allroutes[i]
    #         west = bounds['west']
    #         east = bounds['east']
    #         north = bounds['north']
    #         south = bounds['south']
    #         for stop in bus_route:
    #             STOP = allstops[stop]
    #             slat = STOP["latitude"]
    #             slng = STOP["longitude"]
    #             if (slat >= south and slat <= north) or (slat >= north and slat <= south):
    #                 if (slng >= west and slng <= east) or (slng >= east and slng <= west):
    #                     stop_locations.append({"id": STOP["stopno"], 'lat':slat, 'lng':slng})
    # return HttpResponse(json.dumps({'stop_locations':stop_locations}))

    if request.method == 'POST':
        segments= json.loads(request.body)
        # print(segments)

        seg_stops = {}
        for seg in segments:
            busname = seg['busname']
            startstopname = seg['startstopname']
            startstoplocation = seg['startstoplocation']
            endstopname = seg['endstopname']
            endstoplocation = seg['endstoplocation']
            headsign = seg['headsign']
            numstops = seg['numstops']
            # busname = seg.get('busname')
            # startstopname = seg.get('startstopname')
            # startstoplocation = json.loads(seg.get('startstoplocation'))
            # endstopname = seg.get('endstopname')
            # endstoplocation = json.loads(seg.get('endstoplocation'))
            # headsign = seg.get('headsign')
            # numstops = seg.get('numstops')
            print(busname)
            print(startstopname)
            print(startstoplocation)
            print(endstopname)
            print(endstoplocation)
            print(headsign)
            print(numstops)
            # for stopkey in allstops:
            #     # print(stopkey)
            #     stop_loc = {'lat': allstops[stopkey].get('latitude'), 'lng': allstops[stopkey].get('longitude')}
            #     difference = matchstop(startstoplocation, stop_loc)
            #     if difference['D_lat'] <= 0.000001 and difference['D_lat'] != -1:
            #         # print()
            #         print('--------------------->', allstops[stopkey].get('stopno'))
        # # route_stop_locations = {}
        # for i in bus:
        #     bus_route = allroutes[i]
        #     west = bounds['west']
        #     east = bounds['east']
        #     north = bounds['north']
        #     south = bounds['south']
        #     for stop in bus_route:
        #         STOP = allstops[stop]
        #         slat = STOP["latitude"]
        #         slng = STOP["longitude"]
        #         if (slat >= south and slat <= north) or (slat >= north and slat <= south):
        #             if (slng >= west and slng <= east) or (slng >= east and slng <= west):
        #                 stop_locations.append({"id": STOP["stopno"], 'lat':slat, 'lng':slng})
    return HttpResponse(json.dumps({'stop_locations':"stop_locations"}))


def matchstop(seg, allstops, allroutes):
    busname = seg['busname']
    startstopname = seg['startstopname']
    startstoplocation = seg['startstoplocation']
    endstopname = seg['endstopname']
    endstoplocation = seg['endstoplocation']
    headsign = seg['headsign']
    numstops = seg['numstops']
    pattern = re.compile(r'(?<=stop )\d+\.?\d*')
    alongroutestopids = []
    if len(pattern.findall(startstopname))>0:
        startstopno = pattern.findall(startstopname)
    if len(pattern.findall(endstopname))>0:
        endstopno = pattern.findall(endstopname)
    if startstopno: #if startstopname contains stopno info
        for stopkey in allstops:
            if allstops[stopkey].get('stopno') == startstopno:
                alongroutestopids += slicealongroutestopsid(stopkey, busname, numstops, "start")
                break
    elif endstopno:
        for stopkey in allstops:
            if allstops[stopkey].get('stopno') == endstopno:
                alongroutestopids += slicealongroutestopsid(stopkey, busname, numstops, "end")
                break
    else:
        try:
            for stopkey in allstops:
                stop_loc = {'lat': allstops[stopkey].get('latitude'), 'lng': allstops[stopkey].get('longitude')}
                difference = matchstop(startstoplocation, stop_loc)
                lat_D_val = abs(latlng1['lat']-latlng2['lat'])
                lng_D_val = abs(latlng1['lng']-latlng2['lng'])
        except:
            return {"D_lat": -1, "D_lng": -1}
        return {"D_lat": lat_D_val, "D_lng": lng_D_val}


def gettwostopdistance(loc1, loc2):
    lat_diff = long(loc1.lat - loc2.lat)
def slicealongroutestopsid(longstopid, busname, numstops, start_or_end):
    for route in allroutes:
        if route == busname:
            ROUTE = allroutes[route]
            for in_out in ROUTE:
                for atocode in ROUTE[in_out]:
                    for i in range(0, len(atocode)+1):
                        if atocode[i] == longstopid:
                            if start_or_end == 'start':
                                alongroutestopids = atocode[i:i+numstops+1]
                                return alongroutestopids
                            else:
                                alongroutestopids = atocode[i-numstops:i+1]
                                return alongroutestopids

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

