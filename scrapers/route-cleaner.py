import numpy as np 
import json
import os

def clean_route_data():
    filename = os.path.join(os.path.dirname(__file__),'routes_23_12_2019.txt')

    routeData = np.loadtxt(filename,delimiter='\t',usecols=[14],dtype=str)
    atcoCode = np.loadtxt(filename,delimiter='\t',usecols=[6],dtype=str)
    operator = np.loadtxt(filename,delimiter='\t',usecols=[2],dtype=str)

    routes = []
    data = {}
    for i, routes in enumerate(routeData):
        if operator[i] in ['Dublin Bus','Go-Ahead']:
            data[atcoCode[i]] = dict()
            routelist = routes.split(',')
            routelist[0] = routelist[0][1:]
            routelist[-1] = routelist[-1][:-1]
            data[atcoCode[i]]['routes'] = routelist
            data[atcoCode[i]]['operator'] = operator[i]

    with open('dublinbus/local-bus-data/stop-data.json','w') as outfile:
        json.dump(data,outfile)

    routes = dict()
    for stop in data:
        for route in data[stop]['routes']:
            if route not in routes.keys():
                routes[route] = []
            routes[route] += [stop]

    with open('dublinbus/local-bus-data/route-data.json','w') as outfile:
        json.dump(routes,outfile)

def add_stop_locations():
    filename = os.path.join(os.path.dirname(__file__),'stops_2019_12_23.txt')

    with open('dublinbus/local-bus-data/route-data.json') as infile: 
        routedata = json.load(infile)

    with open('dublinbus/local-bus-data/stop-data.json') as infile: 
        stopdata = json.load(infile)

    atcoCode = np.loadtxt(filename,delimiter='\t',usecols=[0],dtype=str)
    latitude = np.loadtxt(filename,delimiter='\t',usecols=[7],dtype=str)
    longitude = np.loadtxt(filename,delimiter='\t',usecols=[8],dtype=str)

    for i,stopid in enumerate(atcoCode):
        if stopid in stopdata.keys():
            stopdata[stopid]['latitude'] = float(latitude[i])
            stopdata[stopid]['longitude'] = float(longitude[i])

    print(stopdata['8220DB000848'])

    with open('dublinbus/local-bus-data/stop-data.json','w') as outfile:
        json.dump(stopdata,outfile)

clean_route_data()
add_stop_locations()