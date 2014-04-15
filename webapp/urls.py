'''
Created on Apr 4, 2014

@author: Ankit
'''
from django.conf.urls import url

from webapp import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'explorer/', views.explorer, name='explorer'),
    url(r'editor/', views.editor, name='editor'),
    url(r'login/', views.login, name='login'),
    url(r'logout/', views.logout, name='logout'),
    url(r'save/', views.save, name='save'),
    url(r'viewer/(?P<document_id>\d*)', views.viewer, name='viewer'),
    url(r'download/(?P<document_id>\d*)', views.download, name='download')
]