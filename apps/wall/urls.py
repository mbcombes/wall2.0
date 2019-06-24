from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index),      # /
    url(r'^create$', views.create),      # /create
    url(r'^login$', views.login),      # /login
    url(r'^show$', views.show),      # /show
    url(r'^destroy$', views.destroy),      # /destroy
    url(r'^message$', views.message),      # /message
    url(r'^comment$', views.comment),      # /comment
    url(r'^delete$', views.delete),      # /delete
    url(r'^deletemessage$', views.deletemessage),      # /deletemessage
]