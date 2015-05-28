from django.conf.urls import patterns, url, include, handler404
from mileage import views
from mileage.forms import TripStartForm, TripEndForm

urlpatterns = patterns ('',
    url(r'^$', views.TripListView.as_view(), name='list'),
    #url(r'^approve/$', views.TripApproveList.as_view(), name='approve'),
    url(r'^user/$', views.UserListView.as_view(), name='user'),
    #url(r'^d/(?P<pk>\d+)/$', views.TripDetail.as_view(), name='detail'),
    url(r'^supervisor/$', views.SupervisorListView.as_view(), name="sup-list"),
    url(r'^wizard/$', views.TripWizard.as_view(), name="wizard"),
    url(r'^sups/$', views.SupervisorListView.as_view(), name='sups'),
    )
