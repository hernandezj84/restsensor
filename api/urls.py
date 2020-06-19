from django.conf.urls import url
from api import views

urlpatterns = [
    url('^api/test/$', views.test),
    url('^api/event/$', views.create_event),
    url('^', views.test),

]