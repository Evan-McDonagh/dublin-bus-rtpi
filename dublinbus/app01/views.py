import math
import multiprocessing
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
import datetime
from app01 import get_prediction

#  Google Map Apikey
gmap_api = 'AIzaSyB_Bqco2DvRVp55QdFyANIiDRSKS8IE8p8'

#  OpenWeather Forecast Apikey
weather_fore_api = '9570260da25526e20bf66bdf7e1c25e5'

# OpenWeather Preent Apikey
weather_pre_api = 'c9d5929c3180f174f633828540c0fbc5'

dirname = os.path.dirname(__file__)
stopfile = os.path.join(dirname, "../local-bus-data/stop-data.json")
routefile = os.path.join(dirname, "../local-bus-data/all-routes-sequences.json")
scrappedroutefile = os.path.join(dirname, "../local-bus-data/route-data-sequence.json")

with open(routefile) as rt:
    allroutes = json.load(rt)
    rt.close()
with open(stopfile) as st:
    allstops = json.load(st)
    st.close()
with open(scrappedroutefile) as srt:
    scrappedallroutes = json.load(srt)
    srt.close()

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
            print(leap_content)
            context['card_num'] = leap_content.get('card_num')
            context['card_label'] = leap_content.get('card_label')
            context['balance'] = leap_content.get('balance')
            context['card_type'] = leap_content.get('card_type')
            context['expiry_date'] = leap_content.get('expiry_date')

        except:
            context['wrong'] = "wrong"
            # print("the wrong password")
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
        # print(request.body)
        SEGSINFO = json.loads(request.body)
        seg_stops = {}
        segments = SEGSINFO[0]
        bounds = SEGSINFO[1]
        post_alongroutestops = []
        for seg in segments:
            # print(seg)
            if seg['travelmode'].upper() == 'TRANSIT':
                busname = seg['busname']
                if seg['agency'] in ['Dublin Bus', 'Go-Ahead']:
                    numstops = seg['numstops']
                    startstopid = matchstop(seg, allstops)[0]
                    endstopid = matchstop(seg, allstops)[1]
                    alongroutestops = slicealongroutestopsid(startstopid, endstopid, busname, allstops, numstops, bounds)
                    for STOP in alongroutestops:
                        post_alongroutestops.append({"id":STOP['stopno'], 'lat':STOP["latitude"], 'lng':STOP["longitude"]})
                    seg_stops[busname] = post_alongroutestops
                else:
                    try:
                        post_alongroutestops.append({
                            "id": "non-bus-start",
                            'lat':seg['startstoplocation']['lat'],
                            'lng':seg['startstoplocation']['lng'],
                            'non_bus_stopname':seg['agency'] + ":" + seg['startstopname'],
                        })
                        post_alongroutestops.append({
                            "id": "non-bus-end",
                            'lat':seg['endstoplocation']['lat'],
                            'lng':seg['endstoplocation']['lng'],
                            'non_bus_stopname': seg['agency'] + ":" + seg['endstopname'],
                        })
                    except:
                        print('non-bus-info-missed')
                    finally:
                        seg_stops[busname] = post_alongroutestops
            else:
                continue
        # print(seg_stops)
        return JsonResponse(seg_stops, safe=False)


# to match all stops to find the first and the last stop in a a bus segment
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
    startDIST = endDIST = 0.01
    longstopid = ""
    routestopskeys_inbound = allroutes[busname]['Inbound']['atcocodes']
    routestopskeys_outbound = allroutes[busname]['Outbound']['atcocodes']
    routestops = {}
    #  select stop dict from stop-data.json into a dict routestops
    for stopkey in allstops:
        for key in routestopskeys_inbound + routestopskeys_outbound:
            if stopkey == key:
                routestops[stopkey] = allstops[stopkey]
    #
    for stopkey in routestops:
        if routestops[stopkey].get('latitude') is not None:
            stop_loc = {'lat': routestops[stopkey].get('latitude'), 'lng': routestops[stopkey].get('longitude')}
        else:
            print(stopkey, "location does not exist, replaced with {0,0}")
            stop_loc = {'lat': 0, 'lng': 0}
        SD = gettwostopdistance(startstoplocation, stop_loc);
        if SD <= startDIST:
            startDIST = SD
            startstopid = stopkey
        ED = gettwostopdistance(endstoplocation, stop_loc);
        if ED <= endDIST:
            endDIST = ED
            endstopid = stopkey
    if (startstopid in routestopskeys_inbound and endstopid in routestopskeys_inbound) or (startstopid in routestopskeys_outbound and endstopid in routestopskeys_outbound):
        print(startstopid, "---", endstopid)
        return (startstopid, endstopid)
    else:
        print("start stop and endstop are not in same direction")
        return "start stop and endstop are not in same direction"


    # alongroutestopids += slicealongroutestopsid(longstopid, busname, numstops, "start")
    # return alongroutestopids
    # if len(pattern.findall(startstopname)) > 0 and len(pattern.findall(endstopname)) > 0:
    #     startstopno = pattern.findall(startstopname)[0]
    #     endstopno = pattern.findall(endstopname)[0]
    #     print('stopnos', startstopno,'   ',endstopno)
    #     startstopkey = ""
    #     endstopkey = ""
    #     for stopkey in allstops:
    #         if allstops[stopkey].get('stopno') == startstopno:
    #             startstopkey = stopkey
    #             continue
    #         if allstops[stopkey].get('stopno') == endstopno:
    #             endstopkey = stopkey
    #             continue
    #     for route in allroutes:
    #         if route == busname:
    #             ROUTE = allroutes[route]
    #             for in_out in ROUTE:
    #                 atcocodes = ROUTE[in_out]['atcocodes']
    #                 # print(atcocodes)
    #                 if startstopkey in atcocodes and endstopkey in atcocodes:
    #                     print('keys', startstopkey, endstopkey)
    #                     startindex = atcocodes.index(startstopkey)
    #                     endindex = atcocodes.index(endstopkey)
    #                     if startindex <= endindex:
    #                         alongroutestopids = atcocodes[startindex:endindex + 1]
    #                         return alongroutestopids
    #                     else:
    #                         alongroutestopids = atcocodes[endindex:startindex + 1]
    #                         return alongroutestopids
    #                 else:
    #                     continue
    # elif len(pattern.findall(startstopname)) > 0:
    #     startstopno = pattern.findall(startstopname)[0]  # if startstopname contains stopno info
    #     print("start", startstopno)
    #     for stopkey in allstops:
    #         if allstops[stopkey].get('stopno') == startstopno:
    #             alongroutestopids += slicealongroutestopsid(stopkey, busname, numstops, "start")
    #             # print('startno', alongroutestopids)
    #             return alongroutestopids
    # elif len(pattern.findall(endstopname)) > 0:
    #     endstopno = pattern.findall(endstopname)[0]
    #     print("end", endstopno)
    #     for stopkey in allstops:
    #         if allstops[stopkey].get('stopno') == endstopno:
    #             print(stopkey)
    #             alongroutestopids += slicealongroutestopsid(stopkey, busname, numstops, "end")
    #             # print('stopno', alongroutestopids)
    #             return alongroutestopids
    # else:
    #     distance = 0.01
    #     longstopid = ""
    #     routestopskeys = allroutes[busname]['Inbound']['atcocodes'] + allroutes[busname]['Outbound']['atcocodes']
    #     routestops = {}
    #     for stopkey in allstops:
    #         for key in routestopskeys:
    #             if stopkey == key:
    #                 routestops[stopkey] = allstops[stopkey]
    #     for stopkey in routestops:
    #         if routestops[stopkey].get('latitude') is not None:
    #             stop_loc = {'lat': routestops[stopkey].get('latitude'), 'lng': routestops[stopkey].get('longitude')}
    #         else:
    #             print(stopkey, "location does not exist, replaced with {0,0}")
    #             stop_loc = {'lat': 0, 'lng': 0}
    #         DIST = gettwostopdistance(startstoplocation, stop_loc);
    #         if DIST >= distance:
    #             continue
    #         else:
    #             distance = DIST
    #             longstopid = stopkey
    #     alongroutestopids += slicealongroutestopsid(longstopid, busname, numstops, "start")
    #     return alongroutestopids


#  to check if the stop in bounds
def isInbounds(bounds, stop):
    slat = stop['latitude']
    slng = stop['longitude']
    south = bounds['south']
    north = bounds['north']
    west = bounds['west']
    east = bounds['east']
    if (slat >= south and slat <= north) or (slat <= south and slat >= north):
        if (slng >= west and slng <= east) or (slng <= west and slng >= east):
            return True
    return False


#  to get the distance between two stops
def gettwostopdistance(loc1, loc2):
    lat_diff = loc1['lat'] - loc2['lat']
    lng_diff = loc1['lng'] - loc2['lng']
    dist = math.sqrt(pow(lat_diff, 2)+pow(lng_diff, 2))
    return dist


# to extract the sublist in a route sequence list
def slicealongroutestopsid(startstopid, endstopid, busname, allstops, numstops, bounds):
    # print('slicealongroutestopsid---------------------------------------------',startstopid)
    alongroutestops = []
    for route in allroutes:
        if route == busname:
            ROUTE = allroutes[route]
            for in_out in ROUTE:
                atcocodes = ROUTE[in_out]['atcocodes']
                if (startstopid in atcocodes and endstopid in atcocodes):
                    startstopindex = atcocodes.index(startstopid)
                    endstopindex = atcocodes.index(endstopid)
                    print(startstopindex,'****', endstopindex)
                    atcocodes = atcocodes[startstopindex:endstopindex+1]
                    for stopkey in atcocodes:
                        if isInbounds(bounds, allstops[stopkey]):
                            alongroutestops.append(allstops[stopkey])
                    if allstops[startstopid] not in alongroutestops:
                        alongroutestops.append(allstops[startstopid])
                    if allstops[endstopid] not in alongroutestops:
                        alongroutestops.append(allstops[endstopid])
                    return alongroutestops

                # for i in range(0, len(atcocodes)):
                #     if atcocodes[i] == longstopid:
                #         print('i', i, "numstops", numstops, "length", len(atcocodes))
                #         if start_or_end == 'start':
                #             if i+numstops+1 <= len(atcocodes):
                #                 alongroutestopids += atcocodes[i:i+numstops+1]
                #                 return alongroutestopids
                #             else:
                #                 continue
                #         else:
                #             if i-numstops >= 0:
                #                 alongroutestopids += atcocodes[i-numstops:i+1]
                #                 return alongroutestopids
                #             else:
                #                 continue


# show realtime info when a marker alongside the route is clicked
def rtmarkerinfo(request):
    if request.method == 'POST':
        stop_id = request.POST.get('id')
        # print(stop_id)
        url = "https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation" +"?stopid=" + stop_id+"&format=json"
        obj = requests.get(url)
        obj_json = obj.json()
        # # print(stop_id)
        # allinfo = "Stop No." + obj_json.get('stopid') +"<br>"
        # rsp ={obj_json.get('stopid'): []}
        # for result in obj_json['results']:
        #     key = result.get('route')
        #     rsp[obj_json.get('stopid')].append({key: {'arrivaltime':result.get('arrivaldatetime'), 'destination':result.get('destination')}})
        #     allinfo += "Route:"+ key + "  arrive at:" + result.get('arrivaldatetime') + " Towards " + result.get('destination') +"<br>"
        # return HttpResponse(json.dumps({"allinfo":allinfo}))
        # print(obj_json)
    return HttpResponse(json.dumps(obj_json))

# show prediction
def showprediction(request):
    import pickle
    #  just pring some info, but later on, the pkl file can be added and give prediction using info contained in segs.
    if request.method == 'POST':
        segs = json.loads(request.body)
        predictions = []

        datetimedeparture = segs[0]['initialdeparture']
        if datetimedeparture == '':
            datetimedeparture = datetime.datetime.now()
        else:
            datetimedeparture = datetime.datetime.strptime(datetimedeparture, '%Y-%m-%d %H:%M')

        for seg in segs:
            if seg['travelmode'] == 'TRANSIT' and seg['agency'] in ['Dublin Bus', 'Go-Ahead']:
                datestring = datetimedeparture.strftime("%Y-%m-%d %H:%M:%S")
                route = seg['busname'].upper()
                stopA = int(seg['startstopno'])
                stopB = int(seg['endstopno'])

                try:
                    prediction = get_prediction.get_prediction(route, 1, datestring, stopB, stopA)
                except IndexError as e:
                    prediction = get_prediction.get_prediction(route, 2, datestring, stopB, stopA)

                if prediction != None:
                    prediction = int(prediction)
                    datetimedeparture += datetime.timedelta(seconds=prediction)
                else:
                    datetimedeparture += datetime.timedelta(seconds=seg['traveltime'])
                    
                predictions += [prediction]
            else:
                datetimedeparture += datetime.timedelta(seconds=seg['traveltime'])

    print(predictions)
    return HttpResponse(json.dumps({'prediction': predictions}))


# to search a specific route
def routesearch(request):
    if request.method == 'POST':
        route = request.POST.get('route')
        routestopnos = {}
        routestops = {}
        if route in allroutes and route in scrappedallroutes:
            ROUTE = scrappedallroutes[route]
            for in_out in ROUTE:
                key = re.sub('\(.*?\)', '', in_out).replace('  ', ' ').replace('From', '').replace('To', '->')
                scrappeddirstops = ROUTE[in_out]['stops']
                purestopnolist = []
                for stop in scrappeddirstops:
                    purestopnolist.append(stop['stopno'])
                routestopnos[key] = purestopnolist
            # print(routestopnos)
            for in_out in routestopnos:
                in_out_stops = routestopnos[in_out]
                # print(in_out_stops)
                allalongroutestops = []
                # pool = multiprocessing.Pool(6)
                # for i in range(1):
                #     pool.apply_async(func=extractloc, args=(in_out_stops, allalongroutestops), callback=None)
                # pool.close()
                # pool.join()
                extractloc(in_out_stops, allalongroutestops)
                # print(allalongroutestops)
                allalongroutestopslist = allalongroutestops
                # allalongroutestopslist = list(allalongroutestops.intersection(allalongroutestops))
                routestops[in_out] = allalongroutestopslist
        else:
            routestops['Route does not exist'] = 'Route does not exist'
        # print(routestops)
        return HttpResponse(json.dumps(routestops))

# to extract stop details from stop-data.json
def extractloc(routestopnos, allalongroutestops):
    count = 1
    for stopno in routestopnos:
        for stop in allstops:
            STOP = allstops[stop]
            count += 1
            if stopno == STOP['stopno']:
                # print(STOP['stopno'],'-----------',stopno)
                # print('---------------------------------------------------------',stopno)
                # if {"id": STOP['stopno'], 'lat': STOP["latitude"], 'lng': STOP["longitude"]} not in allalongroutestops:
                allalongroutestops.append({"id": STOP['stopno'], 'lat': STOP["latitude"], 'lng': STOP["longitude"]})
    print(count)
    # route_id = request.POST.get('route')
    # routestopids = {}
    # routestops = {}
    # if route_id in allroutes and route_id in scrappedallroutes:
    #     ROUTE = scrappedallroutes[route]
    #     for in_out in ROUTE:
    #         key = re.sub('\(.*?\)', '', in_out).replace('  ', ' ')
    #         routestopids[key] = ROUTE[in_out]['stops']
    # for in_out in routestopids:
    #     key = re.sub('\(.*?\)', '', in_out).replace('  ', ' ')
    #     allalongroutestops = []
    #     in_out_stops = routestopids[in_out]
    #     for i in range(0,len(in_out_stops)):
    #         STOP = allstops[in_out_stops[i]]
    #         allalongroutestops.append({"id": STOP['stopno'], 'lat': STOP["latitude"], 'lng': STOP["longitude"]})
    #     routestops[in_out] = allalongroutestops
    # for route in allroutes:
    #     if route == route_id:
    #         ROUTE = allroutes[route]
    #         for in_out in ROUTE:
    #             routestopids[in_out] = ROUTE[in_out]['atcocodes']
    # for in_out in routestopids:
    #     allalongroutestops = []
    #     in_out_stops = routestopids[in_out]
    #     for i in range(0,len(in_out_stops)):
    #         STOP = allstops[in_out_stops[i]]
    #         allalongroutestops.append({"id": STOP['stopno'], 'lat': STOP["latitude"], 'lng': STOP["longitude"]})
    #     routestops[in_out] = allalongroutestops
    # print(routestops)

# to handle error logger
def errorhandler(request):
    if request.method == 'POST':
        errorinfo = json.loads(request.body)
        print("*********ErrorLogger***********", errorinfo)
        return HttpResponse(json.dumps({}))



