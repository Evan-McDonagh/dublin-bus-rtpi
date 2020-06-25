from django.shortcuts import render,HttpResponse
from app01 import models
from .forms import leapForm,routeForm
from pyleapcard import *
from pprint import pprint
import json
import requests
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