from django.conf.urls import include, url

from . import views

app_name = 'cluster'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^hadoop/on/$', views.hadoopOn, name='hadoopOn'),
    url(r'^hadoop/off/$', views.hadoopOff, name='hadoopOff'),
    url(r'^spark/on/$', views.sparkOn, name='sparkOn'),
    url(r'^spark/off/$', views.sparkOff, name='sparkOff'),
]
