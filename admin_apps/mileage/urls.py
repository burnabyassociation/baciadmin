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
    url(r'^u/(?P<slug>[\w\-]+)/$', views.StaffReimbursementView.as_view()),
    url(r'^d/(?P<slug>[\w\-]+)/$', views.StaffDetailView.as_view(),
    name='staff'),
    )
