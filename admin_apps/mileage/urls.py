from django.conf.urls import patterns, url, include, handler404
from mileage import views
from mileage.forms import TripStartForm, TripEndForm

urlpatterns = patterns ('',
    url(r'^list/$', views.TripListView.as_view(), name='list'),
    url(r'^$', views.TripWizard.as_view(), name="wizard"),
    url(r'^dashboard/$', views.SupervisorDashboardView.as_view(), name='manage'),
    url(r'^(?P<pk>\d+)/edit/$', views.StaffView.as_view(), name='profile'),
    url(r'^(?P<pk>\d+)/edit/approve$', views.ApproveView, name='approve'),
    url(r'^(?P<pk>\d+)/edit/pay$', views.PayView, name='pay'),
    )
