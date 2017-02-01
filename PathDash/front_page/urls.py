from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.front_page),
    url(r'^addons/$', views.addon_front),
    url(r'repeats/$', views.repeats_front),
    url(r'timeflow/$', views.timeflow_front),
    url(r'^levels/$', views.req_levels_front),
    url(r'new_devs/$', views.new_devs),
    url(r'costs/$', views.costs),
    url(r'^ice/$', views.ice),
    url(r'^bundles/$', views.bundles_front),	
]