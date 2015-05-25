from django.conf.urls import patterns, url, include, handler404
from mileage import views

urlpatterns = patterns ('',
    url(r'^$', views.TripList.as_view(), name='list'),
    #url(r'^approve/$', views.TripApproveList.as_view(), name='approve'),
    url(r'^edit/(?P<pk>\d+)/$', views.TripEdit.as_view(), name='edit'),
    url(r'^payperiods/$', views.PayperiodList.as_view(), name="periods")
    #url(r'^d/(?P<pk>\d+)/$', views.TripDetail.as_view(), name='detail'),
    )
