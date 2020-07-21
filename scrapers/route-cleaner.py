import numpy as np 
import json
import os

def clean_route_data():
    """Generates routedata.json file storing bus stop ids, routes served, and operator of bus stop, as taken from all-ireland GTFS file"""
    filename = os.path.join(os.path.dirname(__file__),'data/routes_23_12_2019.txt')

    stopid = np.loadtxt(filename,delimiter='\t',usecols=[0],dtype=str)
    routeData = np.loadtxt(filename,delimiter='\t',usecols=[14],dtype=str)
    direction = np.loadtxt(filename,delimiter='\t',usecols=[5],dtype=str)
    atcoCode = np.loadtxt(filename,delimiter='\t',usecols=[6],dtype=str)
    operator = np.loadtxt(filename,delimiter='\t',usecols=[2],dtype=str)
    name_en = np.loadtxt(filename,delimiter='\t',usecols=[8],dtype=str)
    name_ga = np.loadtxt(filename,delimiter='\t',usecols=[9],dtype=str)

    routes = []
    data = {}
    for i, routes in enumerate(routeData):
        if operator[i] in ['Dublin Bus','Go-Ahead']:
            data[atcoCode[i]] = dict()
            data[atcoCode[i]]['id'] = stopid[i]
            routelist = routes.split(',')
            routelist[0] = routelist[0][1:]
            routelist[-1] = routelist[-1][:-1]
            data[atcoCode[i]]['routes'] = routelist
            data[atcoCode[i]]['operator'] = operator[i]
            data[atcoCode[i]]['direction'] = direction[i]
            ## Dropped bust stop location names due to unicode-related errors 
            # data[atcoCode[i]]['name_en'] = name_en[i]
            # data[atcoCode[i]]['name_ga'] = name_ga[i]


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
    """
        Gets stop locations from dublin bus and go ahead rows of all-ireland gtfs data
        saves to json object in stopdata.json
    """

    filename = os.path.join(os.path.dirname(__file__),'data/stops_2019_12_23.txt')

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

    with open('dublinbus/local-bus-data/stop-data.json','w') as outfile:
        json.dump(stopdata,outfile)

def add_stop_numbers():
    """"
        Fetches stop numebrs and addresses from GTFS text files for Dublin Bus and Go Ahead
        Saves these strings into bus stop objects in stopdata.json
    """
    import codecs

    filename_dublinbus = os.path.join(os.path.dirname(__file__), 'data/stops_dublinbus.txt')
    filename_goahead = os.path.join(os.path.dirname(__file__), 'data/stops_goahead.txt')

    with open('dublinbus/local-bus-data/stop-data.json') as infile: 
        stopdata = json.load(infile)

    def stopdata_from_file(filename,stopdata):
        """Takes filename and stopdata dictionary, adds stop numbers and addresses to dictionary"""
        with codecs.open(filename, encoding='utf8') as file:
            lines_dublin = file.readlines()
            lines_dublin.pop(0)
            for line in lines_dublin:
                line = line.split('"')
                line = list(filter(lambda char: char not in ['',','],line))
                address, atcoCode = line[1], line[0]
                stop_number = address.split(" stop ")[-1]
                address = address.split(", stop ")[0]

                # Error handling for wonky stop numbers, stops not already in JSON file
                try:
                    int(stop_number)
                    try: 
                        stopdata[atcoCode]['stopno'] = stop_number
                        # removing address due to possible unicode bug
                        # stopdata[atcoCode]['address'] = address
                    except KeyError:
                        pass
                        # stopdata[atcoCode] = dict()
                        # stopdata[atcoCode][stop_number] = stop_number
                except:
                    pass
        return stopdata

    stopdata = stopdata_from_file(filename_dublinbus,stopdata)
    stopdata = stopdata_from_file(filename_goahead,stopdata)
    
    for key in stopdata.keys():
        try:
            stopdata[key]['stopno']
        except:
            stopdata[key]['stopno'] = ""

    with open('dublinbus/local-bus-data/stop-data.json','w') as outfile: 
        json.dump(stopdata,outfile)


clean_route_data()
add_stop_locations()
add_stop_numbers()