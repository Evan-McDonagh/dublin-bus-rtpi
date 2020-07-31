import multiprocessing

from django.test import TestCase

# Create your tests here.

import math
import re

from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from app01 import models
# from .forms import leapForm,routeForm
from pyleapcard import *
from pprint import pprint
import json
import requests
import re
import os
import datetime
from app01 import get_prediction
from multiprocessing import Pool

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

# to search a specific route
def routesearchtest(id):
    if True:
        route = id
        routestopnos = {}
        routestops = {}
        if route in allroutes and route in scrappedallroutes:
            ROUTE = scrappedallroutes[route]
            stopkeyRoute = allroutes[route]
            for in_out in ROUTE:
                key = re.sub('\(.*?\)', '', in_out).replace('  ', ' ')
                scrappeddirstops = ROUTE[in_out]['stops']
                purestopnolist = []
                for stop in scrappeddirstops:
                    purestopnolist.append(stop['stopno'])
                routestopnos[key] = purestopnolist
        print(routestopnos)
        for in_out in routestopnos:
            in_out_stops = routestopnos[in_out]
            # print(in_out_stops)
            allalongroutestops = []
            pool = multiprocessing.Pool(6)
            # for i in range(1):
            #     pool.apply_async(func=extractloc, args=(in_out_stops, allalongroutestops), callback=None)
            # pool.close()
            # pool.join()
            extractloc(in_out_stops, allalongroutestops)
            # print(allalongroutestops)
            allalongroutestopslist = allalongroutestops
            # allalongroutestopslist = list(allalongroutestops.intersection(allalongroutestops))
            routestops[in_out] = allalongroutestopslist
        print(routestops)

            # for i in range(0,len(in_out_stops)):
            #
            #     STOP = allstops[in_out_stops[i]]
        #         allalongroutestops.append({"id": STOP['stopno'], 'lat': STOP["latitude"], 'lng': STOP["longitude"]})
        # return HttpResponse(json.dumps(routestops))

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
# def listappend(dict):
#     allalongroutestops.add
routesearchtest('11')