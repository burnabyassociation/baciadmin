from django.conf.urls import patterns, url, include, handler404
from mileage import views
from mileage.forms import TripStartForm, TripEndForm

urlpatterns = patterns ('',
    url(r'^$', views.TripListView.as_view(), name='list'),
    #url(r'^approve/$', views.TripApproveList.as_view(), name='approve'),
    url(r'^edit/(?P<pk>\d+)/$', views.TripEditView.as_view(), name='edit'),
    #url(r'^d/(?P<pk>\d+)/$', views.TripDetail.as_view(), name='detail'),
    url(r'^supervisor/$', views.SupervisorFormView.as_view(), name="sup-list"),
    url(r'^wizard/$', views.TripWizard.as_view(), name="wizard"),
    )
