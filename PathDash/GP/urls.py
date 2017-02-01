from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.gpfront),
    url(r'cost/$', views.costfront),
    url(r'cost/costs_bubble/$', views.costs_bubble),
    url(r'cost/costxgp/', views.costxgp),
    url(r'^rlevels/$', views.r_front),
    url(r'^rlevels/by_location/$', views.r_by_location),
    url(r'^rlevels/boxplots/$', views.boxplots_set_by_loc),
    url(r'^ice/$', views.ice_front),
    url(r'^ice/by_location/$', views.ice_by_location)	
    ]