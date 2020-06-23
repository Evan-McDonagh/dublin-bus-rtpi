from django.shortcuts import render,HttpResponse

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

# load_bus_data()