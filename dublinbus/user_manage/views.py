import re

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
        fn = request.POST.get('firstname')
        ln = request.POST.get('lastname')
        password = request.POST.get('pwd')
        password_cfm = request.POST.get('pwdcfm')
        email = request.POST.get('email')
        phone = request.POST.get('txtEmpPhone')
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        gender = request.POST.get('gender')

        # allow = request.POST.get('allow')

        # verify data
        # verify the first name
        if fn == "":
            # first name not received
            return render(request, 'register.html', {'errmsg': 'Lack of First name '})

        # verify the last name
        if ln == "":
            # last name not received
            return render(request, 'register.html', {'errmsg': 'Lack of Last name '})

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
    #     if allow != 'on':
    #         return render(request, 'register.html', {'errmsg': '请同意协议'})
    #
        # check is a user with same name has been registered
        try:
            users = User.objects.filter(fname=fn).filter(lname=ln)
        except:
            # user does not exist
            users = None

        if users:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': 'user already exists'})

    #     # 进行业务处理: 进行用户注册
        user = User()
        user.fname = fn
        user.lname = ln
        user.password = make_password(password)
        user.email = email
        user.question = question
        if phone != "":
            user.phone = phone
        user.answer = answer
        user.gender = gender
        user.isDelete = False
        user.save()

        print(fn)
        print(ln)
        print(password)
        print(password_cfm)
        print(email)
        print(phone)
        print(question)
        print(answer)
        print(gender)
    #
        # 返回应答, 跳转到首页
        return redirect(reverse('app01:index'))
    #
    # return render(request, 'register.html', {'errmsg': 'error message'})
    # return HttpResponse({'errmsg':'error message'})
    # return HttpResponse({'errmsg':'error message'})
