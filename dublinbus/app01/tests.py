import multiprocessing

from django.test import TestCase,Client

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


from django.test import SimpleTestCase
from django.urls import reverse,resolve
from app01.views import *

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
# def routesearchtest(id):
#     if True:
#         route = id
#         routestopnos = {}
#         routestops = {}
#         if route in allroutes and route in scrappedallroutes:
#             ROUTE = scrappedallroutes[route]
#             stopkeyRoute = allroutes[route]
#             for in_out in ROUTE:
#                 key = re.sub('\(.*?\)', '', in_out).replace('  ', ' ')
#                 scrappeddirstops = ROUTE[in_out]['stops']
#                 purestopnolist = []
#                 for stop in scrappeddirstops:
#                     purestopnolist.append(stop['stopno'])
#                 routestopnos[key] = purestopnolist
#         print(routestopnos)
#         for in_out in routestopnos:
#             in_out_stops = routestopnos[in_out]
#             # print(in_out_stops)
#             allalongroutestops = []
#             pool = multiprocessing.Pool(6)
#             # for i in range(1):
#             #     pool.apply_async(func=extractloc, args=(in_out_stops, allalongroutestops), callback=None)
#             # pool.close()
#             # pool.join()
#             extractloc(in_out_stops, allalongroutestops)
#             # print(allalongroutestops)
#             allalongroutestopslist = allalongroutestops
#             # allalongroutestopslist = list(allalongroutestops.intersection(allalongroutestops))
#             routestops[in_out] = allalongroutestopslist
#         print(routestops)

#             # for i in range(0,len(in_out_stops)):
#             #
#             #     STOP = allstops[in_out_stops[i]]
#         #         allalongroutestops.append({"id": STOP['stopno'], 'lat': STOP["latitude"], 'lng': STOP["longitude"]})
#         # return HttpResponse(json.dumps(routestops))

# def extractloc(routestopnos, allalongroutestops):
#     count = 1
#     for stopno in routestopnos:
#         for stop in allstops:
#             STOP = allstops[stop]
#             count += 1
#             if stopno == STOP['stopno']:
#                 # print(STOP['stopno'],'-----------',stopno)
#                 # print('---------------------------------------------------------',stopno)
#                 # if {"id": STOP['stopno'], 'lat': STOP["latitude"], 'lng': STOP["longitude"]} not in allalongroutestops:
#                 allalongroutestops.append({"id": STOP['stopno'], 'lat': STOP["latitude"], 'lng': STOP["longitude"]})
#     print(count)
# def listappend(dict):
#     allalongroutestops.add
# routesearchtest('11')



#test urls
class TestUrls(SimpleTestCase):
    def testLeapcard(self):
        url = reverse('app01:leapcard')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,leapcard)

    
    def testStop(self):
        url = reverse('app01:stop')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,stop)

    def testInit(self):
        url = reverse('app01:init')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,init)

    def testWeather(self):
        url = reverse('app01:weather')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,weather)
    
    def testRtmarkerinfo(self):
        url = reverse('app01:rtmarkerinfo')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,rtmarkerinfo)

    def testShowprediction(self):
        url = reverse('app01:showprediction')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,showprediction)
    
    def testRoutesearch(self):
        url = reverse('app01:routesearch')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,routesearch)
    

#test leapcard function
class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.leapcard_url = reverse('app01:leapcard')
        self.stop_url = reverse('app01:stop')
        self.init_url = reverse('app01:init')
        self.weather_url = reverse('app01:weather')
        self.rtmarkerinfo_url = reverse('app01:rtmarkerinfo')
        self.routesearch_url = reverse('app01:routesearch')

    #test leapcard function
    def test_Leapcard_GET(self):
        response = self.client.get(self.leapcard_url)  

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_Leapcard_POST(self):
        response = self.client.post(self.leapcard_url,{
            'username': "admin",
            'password': "111111",
        })  

        self.assertEquals(response.status_code,200)
        # print(response.content)  #print the worng messsage
    
    #test stop function
    def test_Stop_GET(self):
        response = self.client.get(self.stop_url)  

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_Stop_POST(self):
        response = self.client.post(self.stop_url,{
            'stop_id': "271",
        })  

        self.assertEquals(response.status_code,200)
        # print(response.content)  #print the worng messsage

    #test init function
    def test_INIT_GET(self):
        response = self.client.get(self.init_url)  

        self.assertEquals(response.status_code,200)

        
    def test_INIT_POST(self):
        response = self.client.post(self.init_url,{
            'lat' : 53.3200896,
            'lng' : -6.2521344,
        })  

        self.assertEquals(response.status_code,200)   

    #test weather function
    def test_WEATHER_GET(self):
        response = self.client.get(self.weather_url)  

        self.assertEquals(response.status_code,200)


    def test_WEATHER_POST(self):
        response = self.client.post(self.weather_url,{
            'lat' : 53.3200896,
            'lng' : -6.2521344,
        })  

        self.assertEquals(response.status_code,200)  

    
    def test_Rtmarkerinfo_POST(self):
        response = self.client.post(self.rtmarkerinfo_url,{
            'id': "271",
        })  
        self.assertEquals(response.status_code,200) 
    
    
    def test_Routesearch_POST(self):
        response = self.client.post(self.routesearch_url,{
            'route': "11",
        })  

        self.assertEquals(response.status_code,200)
    
