'''
Created on Apr 4, 2014

@author: Ankit
'''
from django.conf.urls import url

from webapp import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]