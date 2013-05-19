from django.conf.urls import patterns, include, url
from django.contrib import admin
from allotments.api.views import AllotmentList, AllotmentDetail, GeoAllotmentList, GeoAllotmentDetail


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('allotments.api.views',
    url(r'^api/$', 'api_root'),
)

#api url patterns, make them work with or without a trailing /
urlpatterns += patterns('',
    url(r'^api/allotments/$', AllotmentList.as_view(), name='allotment-list'),
    url(r'^api/allotments$', AllotmentList.as_view(), name='allotment-list'),
    url(r'^api/allotments/(?P<pk>\d+)/$', AllotmentDetail.as_view(), name='allotment-detail'),
    url(r'^api/allotments/(?P<pk>\d+)$', AllotmentDetail.as_view(), name='allotment-detail'),
    url(r'^api/geo/allotments/$', GeoAllotmentList.as_view(), name='allotment-list'),
    url(r'^api/geo/allotments$', GeoAllotmentList.as_view(), name='allotment-list'),
    url(r'^api/geo/allotments/(?P<pk>\d+)/$', GeoAllotmentDetail.as_view(), name='allotment-detail'),
    url(r'^api/geo/allotments/(?P<pk>\d+)$', GeoAllotmentDetail.as_view(), name='allotment-detail'),
)

# Default login/logout views
urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

urlpatterns += patterns('allotments.views',
    url(r'list/$', 'list'),
    url(r'map/$', 'mapView'),
)