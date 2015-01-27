from django.conf.urls import patterns, include, url
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import BaseDetailView
from hotels.models import Hotel
from hotels.views import HotelSearchView, HotelUpdate, HotelView

hotel_patterns = patterns(
    '',
    url(r'^update/$', HotelUpdate.as_view(), name='hotel_edit'),
    url(r'^view/$', HotelView.as_view(), name='hotel_view'),
)

urlpatterns = patterns(
    '',
    url(r'^$', ListView.as_view(model=Hotel), name='hotel_list'),
    url(r'^search/$', HotelSearchView.as_view(), name='hotel_search'),
    url(r'^(?P<pk>\d+)/', include(hotel_patterns)),
    url(r'^roomClass/$', (lambda: None), name='hotel_room_class_edit'),
    url(r'^new/$', (lambda: None), name='hotel_new'),
    url(r'^approve/$', (lambda: None), name='hotel_approve'),
)
