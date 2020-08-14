from django.test import TestCase,Client

from django.test import SimpleTestCase
from django.urls import reverse,resolve
from user_manage.views import *

# Create your tests here.
class TestUrls(SimpleTestCase):
    def testRegister(self):
        url = reverse('user_manage:register')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,register)

    
    def testLogin(self):
        url = reverse('user_manage:login')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,login)

    def testLogout(self):
        url = reverse('user_manage:logout')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,logout)

    def testAddfav(self):
        url = reverse('user_manage:addfav')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,addfav)
    
    def testShowuserinfowindow(self):
        url = reverse('user_manage:showuserinfowindow')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,showuserinfowindow)

    def testGetfav(self):
        url = reverse('user_manage:getfav')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,getfav)
    
    def testDelfav(self):
        url = reverse('user_manage:delfav')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,delfav)
    
    def testCheckstatus(self):
        url = reverse('user_manage:checkstatus')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,checkstatus)
    
    def testTest(self):
        url = reverse('user_manage:test')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,test)


