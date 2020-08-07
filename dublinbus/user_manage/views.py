import re

from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from user_manage.models import User
from django.utils import timezone
from datetime import *
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.


def register(request):
    '''Register'''
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

        return render(request, 'login.html', {'alertinfo': 'Welcome to DublinbusTeam2', 'username': username})


def login(request):
    """Register"""
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
        # receive data
        username = request.POST.get('username')
        password = request.POST.get('password')

        # check data
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': 'username or password missed'})

        # start verifying the data is correct
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            # password is correct
            # set session
            request.session['userid'] = user.id
            request.session.set_expiry(0)   # when the user close the browser the session will expired

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

            # print(request.session.get('userid'))
            # return response
            return render(request, "userinfo.html", {'username': username})
        else:
            # password is wrong
            return render(request, 'login.html', {'errmsg': 'username does not match password'})


def logout(request):
    if request.method == 'POST':
        try:
            print(request.session['userid'])
            del request.session['userid']
        except KeyError:
            pass
        # try:
        #     print(request.session['userid'])
        # except KeyError:
        #     print('keyerror')
        return redirect(reverse('app01:index'))


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