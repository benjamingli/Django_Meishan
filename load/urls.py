from django.conf.urls import include, url

from . import views

app_name = 'load'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^weather/$', views.weather, name='weatherRoot'),
    url(r'^weather/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', views.weather, name='weather'),
    url(r'^weather/(?P<year>[0-9]+)-(?P<month>[0-9]+)-(?P<day>[0-9]+)/del/$', views.weatherDel),
    url(r'^weather/conf/$', views.weatherConf, name='weatherConf'),
    url(r'^rawCsv/$', views.rawCsv, name='rawCsv'),
    url(r'^rawCsv/(?P<fullname>[^/]+)/del/$', views.rawCsvDel),
    url(r'^rawCsv/conf/$', views.rawCsvConf, name='rawCsvConf'),
    url(r'^data/$', views.data, name='data'),
    url(r'^data/(?P<fullname>[^/]+)/del/$', views.dataDel),
    url(r'^data/conf/$', views.dataConf, name='dataConf'),
    url(r'^result/$', views.result, name='result'),
    url(r'^result/(?P<id_num>[0-9]+)/$', views.resultDetail, name='detail'),
    url(r'^result/(?P<id_num>[0-9]+)/del/$', views.resultDel),
    url(r'^result/conf/$', views.resultConf, name='resultConf'),
]
