import numpy as np 
import json
import os

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

routes = dict()
for stop in data:
    for route in data[stop]['routes']:
        if route not in routes.keys():
            routes[route] = []
        routes[route] += [stop]

with open('dublinbus/local-bus-data/route-data.json','w') as outfile:
    json.dump(routes,outfile)