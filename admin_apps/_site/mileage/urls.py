from django.conf.urls import patterns, url, include, handler404
from mileage import views

urlpatterns = patterns ('',
    url(r'^$', views.TripList.as_view(), name='list'),
    url(r'^edit/(?P<pk>\d+)/$', views.TripEdit.as_view(), name='edit'),
    #url(r'^d/(?P<pk>\d+)/$', views.TripDetail.as_view(), name='detail'),
    )
