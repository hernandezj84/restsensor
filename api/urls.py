from django.conf.urls import url
from api import views

urlpatterns = [
    url('^api/test/$', views.test),
]