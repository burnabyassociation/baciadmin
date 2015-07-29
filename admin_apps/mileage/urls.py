from django.conf.urls import patterns, url, include, handler404
from mileage import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns ('',
    url(r'^$', views.ReimbursementListView.as_view(), name="home"),
    url(r'^r/create$', views.ReimbursementCreateView.as_view(), name="create_reimbursement"),
    url(r'^del/(?P<pk>\d+)$', views.TripDeleteView.as_view(), name='delete_trip'),
    url(r'^r/(?P<pk>\d+)$', views.TripListView.as_view(), name='detail_reimbursement'),
    url(r'^del/r/(?P<pk>\d+)$', views.ReimbursementDeleteView.as_view(), name='delete_reimbursement'),
    ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
