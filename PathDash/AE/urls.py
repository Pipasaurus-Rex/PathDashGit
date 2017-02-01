from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.graphs_front),
    url(r'^addons/$', views.addons),
    url(r'^addons/details/', views.addon_test_detail),
    url(r'^addons/cost/', views.addon_cost),
    url(r'^repeat/', views.repeats),
    url(r'^repeats/details/', views.repeats_detail),
    url(r'^test/$', views.test),
    url(r'^timeflow/$', views.timeflow),
    url(r'^compare/', views.compare),
    url(r'^icd_split/', views.icd_split),
    url(r'^costs_bubble/', views.costs_bubble),
    url(r'^(?P<source>\w{1,50})/costxtime/', views.costxtime),
    url(r'^ice/$', views.ice_count),
    url(r'^not_ice/', views.not_ice_count),
    url(r'^ice_n/', views.ice),
    url(r'^bundles/$', views.bundles),
    url(r'^(?P<source>\w{1,50})/requesting_levels/', views.requesting_levels),
]