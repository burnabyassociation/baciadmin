from django.conf.urls import patterns, url, include, handler404
from mileage import views
from mileage.forms import TripStartForm, TripEndForm

urlpatterns = patterns ('',
    url(r'^$', views.TripListView.as_view(), name='list'),
    #url(r'^approve/$', views.TripApproveList.as_view(), name='approve'),
    url(r'^user/$', views.UserListView.as_view(), name='user'),
    #url(r'^d/(?P<pk>\d+)/$', views.TripDetail.as_view(), name='detail'),
    url(r'^wizard/$', views.TripWizard.as_view(), name="wizard"),
    url(r'^dashboard/$', views.SupervisorDashboardView.as_view(), name='supervisor'),
    url(r'^u/(?P<slug>[\w\-]+)/$', views.StaffReimbursementView.as_view(), name='staff'),
    url(r'^remove/(?P<talklist_pk>\d+)/(?P<pk>\d+)/$',
    views.TripDeleteView.as_view(),
    name='remove_trip'),
    url(r'^(?P<pk>\d+)/edit/$', views.StaffView.as_view(), name='profile'),
    )
