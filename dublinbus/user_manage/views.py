import json
import os
import re

from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from user_manage.models import User, Places, Stops, Routes, Leapcard
from django.utils import timezone
from datetime import *
from django.contrib.auth.hashers import make_password, check_password


def register(request):
    """Register"""
    if request.method == 'GET':
        # show register page
        return render(request, 'register.html')
    else:
        # process the register flow

        # receive data
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        password_cfm = request.POST.get('pwdcfm')
        email = request.POST.get('email')
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        gender = request.POST.get('gender')

        # allow = request.POST.get('allow') # choose to agree with the user agreement or not

        # verify data
        # verify the user name
        if username == "":
            # user name not received
            return render(request, 'register.html', {'errmsg': 'Lack of user name '})

        # verify password
        if password == "":
            # password not received
            return render(request, 'register.html', {'errmsg': 'Lack of password'})

        # verify password == password confirm
        if password != password_cfm:
            # passwords do not equal
            return render(request, 'register.html', {'errmsg': 'passwords do not equal'})

        # verify email
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': 'email format is not correct'})

        # verify question
        if question == "Please select your Sequrity Question":
            # passwords do not equal
            return render(request, 'register.html', {'errmsg': 'security question is not chosen'})

        # verify answer
        if answer == "":
            # passwords do not equal
            return render(request, 'register.html', {'errmsg': 'security question is not answered'})
        #
        #     if allow != 'on': # the user agree with the user agreement
        #         return render(request, 'register.html', {'errmsg': 'Please agree with the user agreement'})

        # check is a user with same name has been registered
        try:
            user = User.objects.get(name=username)
        except:
            # user does not exist
            user = None

        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': 'user already exists'})

        #  process the registration slow
        user = User()
        user.name = username
        user.password = make_password(password)
        user.email = email
        user.question = question
        user.answer = answer
        user.gender = gender
        user.isDelete = False
        user.save()

        # print(username)
        # print(password)
        # print(password_cfm)
        # print(email)
        # print(question)
        # print(answer)
        # print(gender)

        # render the web page to index
        # return redirect(reverse('app01:index'))
        # request.session['userid'] = user.id

        return render(request, 'login.html', {'alertinfo': 'Welcome to DublinbusTeam2', 'username': username})


def login(request):
    """login"""
    if request.session.get('username') != None:
        print('login session', request.session.get('username'))
        return render(request, "userindex.html", {'username': request.session.get('username')})
    # the request from other pages
    if request.method == 'GET':
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
        else:
            username = ''
        # show register page
        return render(request, 'login.html', {'username': username})
    # the request is from login html form
    elif request.method == 'POST':
        '''login verify'''
        username = request.POST.get('username')
        password = request.POST.get('password')
        if request.session.get('username') == username:
            print('login session', request.session.get('username'))
            return render(request, "userindex.html", {'username': request.session.get('username')})
        # receive data

        # check data
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': 'username or password missed'})

        # check whether the user is a registered user.
        try:
            user = User.objects.get(name=username)
        except:
            user = None
        if user == None:
            return render(request, 'login.html', {'errmsg': 'Username does not exist, cilck "register" to become a registered user.'})
            # return HttpResponse({'errmsg': 'Username does not exist, cilck "register" to become a registered user.'})

        # start verifying the data is correct
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            # password is correct
            # set session
            request.session['username'] = user.name
            request.session.set_expiry(60*10)   # when the user close the browser the session will expired

            # login success, render the web page to index
            next_url = request.GET.get('next', reverse('app01:index'))

            # turn to next_url
            response = redirect(next_url, {'username': username})  # HttpResponseRedirect

            # remember the user name or not
            remember = request.POST.get('remember')
            if remember == 'on':
                # set cookie to store the username
                response.set_cookie('username', username, max_age=7 * 24 * 3600)
            else:
                response.delete_cookie('username')

            print(request.session.get('username'))

            context = load_bus_data()
            context['username'] = username
            print(context)
            # return response
            return render(request, "userindex.html", context)
            # return render(request, "userindex.html", {'username': username})
        else:
            # password is wrong
            return render(request, 'login.html', {'errmsg': 'username does not match password', "username":username})


class UserLoginBackend(ModelBackend):
    """ define a verification backend  """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # print(username)
        # print(password)
        # print(User.objects.get(Q(name=username) | Q(email=username)))
        try:
            user = User.objects.get(Q(name=username) | Q(email=username))
            # print(user.password)
            if check_password(password, user.password):
                return user
        except Exception as e:
            return None


def logout(request):
    if request.method == 'POST':
        print('Going to logout')
        try:
            print(request.session['username'])
            # del request.session['userid'] # del do not delete session data from session table
            request.session.flush()   # flush delete session data data from session table
            # request.session.clear()  # clear do not delete session data from session table
        except KeyError:
            pass
        try:
            print(request.session['username'])
        except KeyError:
            print('keyerror')
            # return HttpResponse(json.dumps({'msg': "logout failed"}))
        return render(request, "index.html")

        # return render(request, 'index.html')


def addmyplace(username, place):
    # if request == 'POST':
    print('addpalce')
    try:
        user = User.objects.get(name=username)
    except:
        user = None
    if user == None:
        # return HttpResponse(json.dumps({'msg': username + "is not a registered user."}))
        return json.dumps({'msg': username + "is not a registered user."})
    else:
        try:
            Place = Places.objects.filter(username_id=username, place=place)
        except:
            Place = []
        print(Place)
        if len(Place) == 0:
            myplace = Places.objects.create(username_id=username, place=place)
            # return HttpResponse(json.dumps({'msg': "favorite place added successfully!"}))
            return json.dumps({'msg': "favorite place added successfully!"})
        else:
            return json.dumps({'msg': "this place is already stored in your aount"})


def addmystop(username, stop):
    # if request == 'POST':
    #     if request == 'POST':
    print('addstop')
    try:
        user = User.objects.get(name=username)
    except:
        user = None
    if user == None:
        # return HttpResponse(json.dumps({'msg': username + "is not a registered user."}))
        return json.dumps({'msg': username + "is not a registered user."})
        # msg = {'msg': username + "is not a registered user."}
        # return msg
    else:
        try:
            Stop = Stops.objects.filter(username_id=user.name, stop=stop)
        except:
            Stop = []
        print(Stop)
        if len(Stop) == 0:
            mystop = Stops.objects.create(username_id=user.name, stop=stop)
            # return HttpResponse(json.dumps({'msg': "favorite place added successfully!"}))
            return json.dumps({'msg': "favorite stop added successfully!"})
        else:
            return json.dumps({'msg': "this stop is already stored in your account"})



def addmyroute(username, route):
    # if request == 'POST':
    #     if request == 'POST':
    print('addroute')
    try:
        user = User.objects.get(name=username)
    except:
        user = None
    if user == None:
        # return HttpResponse(json.dumps({'msg': username + "is not a registered user."}))
        print('none')
        print(json.dumps({'msg': username + "is not a registered user."}))
        return json.dumps({'msg': username + "is not a registered user."})
    else:
        print('user exists', user.name)
        try:
            Route = Routes.objects.filter(username_id=user.name, route=route)
        except:
            Route = []
        print(Route)
        if len(Route) == 0:
            myroot = Routes.objects.create(username_id=user.name, route=route)
            # return HttpResponse(json.dumps({'msg': "favorite route added successfully!"}))
            print(json.dumps({'msg': "favorite route added successfully!"}))
            return json.dumps({'msg': "favorite route added successfully!"})
        else:
            return json.dumps({'msg': "this route is already stored in your account"})


def addmyleapcard(username, cardholder):
    # if request == 'POST':
    #     if request == 'POST':
    print('addmyleapcard')
    try:
        user = User.objects.get(name=username)
    except:
        user = None
    if user == None:
        # return HttpResponse(json.dumps({'msg': username + "is not a registered user."}))
        print('none')
        print(json.dumps({'msg': username + "is not a registered user."}))
        return json.dumps({'msg': username + "is not a registered user."})
    else:
        print('user exists', user.name)
        try:
            leapcard = Leapcard.objects.filter(username_id=user.name, leapcard=cardholder)
        except:
            leapcard = []
        print(leapcard)
        if len(leapcard) == 0:
            myleapcard = Leapcard.objects.create(username_id=user.name, leapcard=cardholder)
            # return HttpResponse(json.dumps({'msg': "favorite route added successfully!"}))
            print(json.dumps({'msg': "leapcard holder info added successfully!"}))
            return json.dumps({'msg': "leapcard holder info added successfully!"})
        else:
            return json.dumps({'msg': "leapcard holder info is already stored in your account"})

def addfav(request):
    if request.method == 'POST':
        # print('addfav')
        choice = request.POST.get('choice')
        content = request.POST.get('content')
        username = request.POST.get('username')
        try:
            username_session = request.session.get('username')
        except:
            username_session = None
        print(username_session)
        if username_session == None:
            msg = json.dumps({'msg': 'please refresh and login to your account'})
            # return render(request, 'index.html')
            return HttpResponse(msg)
        if choice == "place":
            msg = addmyplace(username, content)
            print(msg)
            return HttpResponse(msg)
        if choice == "stop":
            msg = addmystop(username, content)
            print(msg)
            return HttpResponse(msg)
        if choice == 'route':
            msg = addmyroute(username, content)
            print(msg)
            return HttpResponse(msg)
        if choice == 'leapcard':
            msg = addmyleapcard(username, content)
            print(msg)
            return HttpResponse(msg)
        else:
            msg = json.dumps({'msg':"wrong added data type"})
            return HttpResponse(msg)

def getfav(request):
    if request.method == 'POST':
        # print('addfav')
        choice = request.POST.get('choice')
        # content = request.POST.get('content')
        username = request.POST.get('username')
        try:
            username_session = request.session.get('username')
        except:
            username_session = None
        print(username_session)
        if username_session == None:
            msg = json.dumps({'msg': 'please login to your account'})
            return render(request, 'index.html')
            # return HttpResponse(msg)
        gainedcontents = []
        if choice == "place":
            places = Places.objects.filter(username_id=username)
            for place in places:
                gainedcontents.append(place.place)
            msg = json.dumps({'content': gainedcontents})
        elif choice == "stop":
            stops = Stops.objects.filter(username_id=username)
            for stop in stops:
                gainedcontents.append(stop.stop)
            msg = json.dumps({'content': gainedcontents})
        elif choice == 'route':
            routes = Routes.objects.filter(username_id=username)
            for route in routes:
                gainedcontents.append(route.route)
            msg = json.dumps({'content': gainedcontents})
        else:
            msg = json.dumps({'msg': "wrong added data type"})
        print(msg)
        return HttpResponse(msg)

def showuserinfowindow(request):
    if request.method == 'POST':
        # print('addfav')
        choice = request.POST.get('choice')
        content = request.POST.get('content')
        username = request.POST.get('username')
        try:
            username_session = request.session.get('username')
        except:
            username_session = None
        print(username_session)
        if username_session == None:
            # msg = json.dumps({'msg':'please lonin to your account'})
            return render(request, 'index.html', {'msg':'please login to your account'})

        try:
            user = User.objects.get(name=username)
        except:
            user = None
        if user == None:
            print('none')
            print(json.dumps({'msg': username + "is not a registered user."}))
            return HttpResponse(json.dumps({'msg': username + "is not a registered user."}))
            # return render(request, 'userindex.html', {'msg':username + "is not a registered user."})
        else:
            print('user exists', user.name)
            places = []
            stops = []
            routes = []
            leapcards = []

            placesfilt = Places.objects.filter(username_id=user.name)
            for place in placesfilt:
                places.append(place.place)

            stopsfilt = Stops.objects.filter(username_id=user.name)
            for stop in stopsfilt:
                stops.append(stop.stop)

            routesfilt = Routes.objects.filter(username_id=user.name)
            for route in routesfilt:
                routes.append(route.route)

            leapcardfilt = Leapcard.objects.filter(username_id=user.name)
            for cardholder in leapcardfilt:
                leapcards.append(cardholder.leapcard)
            print(places)
            print(stops)
            print(routes)
            print(leapcards)
            # return render(request, 'userindex.html', {'palces':places, 'stops':stops, 'routes':routes})
            return HttpResponse(json.dumps({'places':places, 'stops':stops, 'routes':routes, 'leapcards':leapcards}))

def delfav(request):
    if request.method == 'POST':
        # print('addfav')
        choice = request.POST.get('choice')
        content = request.POST.get('content')
        username = request.POST.get('username')
        try:
            username_session = request.session.get('username')
        except:
            username_session = None
        print(username_session)
        if username_session == None:
            # msg = json.dumps({'msg':'please refresh and login to your account'})
            return render(request, 'index.html')
            return HttpResponse(msg)
        if choice == "place":
            Places.objects.get(username_id=username, place=content).delete()
            msg = json.dumps({'msg': "place deleted successfully!"})
            print(msg)
            return HttpResponse(msg)
        if choice == "stop":
            Stops.objects.get(username_id=username, stop=content).delete()
            msg = json.dumps({'msg': "stop deleted successfully!"})
            print(msg)
            return HttpResponse(msg)
        if choice == 'route':
            Routes.objects.get(username_id=username, route=content).delete()
            msg = json.dumps({'msg': "route deleted successfully!"})
            print(msg)
            return HttpResponse(msg)
        if choice == 'leapcard':
            Leapcard.objects.get(username_id=username, leapcard=content).delete()
            msg = json.dumps({'msg': "leapcard deleted successfully!"})
            print(msg)
            return HttpResponse(msg)
        else:
            msg = json.dumps({'msg':"wrong data type"})
            return HttpResponse(msg)


def checkstatus(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        try:
            username_session = request.session.get('username')
        except:
            username_session = None
        print(username_session)
        if username_session == None:
            isLogin = json.dumps({'isLogin': 'no'})
            return HttpResponse(isLogin)
        if uname != username_session:
            isLogin = json.dumps({'isLogin': 'no'})
            return HttpResponse(isLogin)
        else:
            isLogin = json.dumps({'isLogin': 'yes'})
            return HttpResponse(isLogin)
            # return render(request, 'index.html', {'msg':'please login to your account'})

def test(request):
    if request.method == 'POST':
        print('addfav')
        return HttpResponse(json.dumps({'msg':"test"}))


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