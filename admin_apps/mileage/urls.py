from __future__ import absolute_import

from django.conf.urls import patterns, url, include, handler404
from mileage import views

urlpatterns = patterns ('',
    #url(r'^create/$', views.TripCreate.as_view(), name='create'),
    url(r'^$', views.TripList.as_view(), name='list'),
    #url(r'^d/(?P<pk>\d+)/$', views.TripDetail.as_view(), name='detail'),
    )
