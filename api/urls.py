from django.conf.urls import url
from api import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url('^api/test/$', views.test),
    url('^api/event/$', views.create_event),
    url('^api/registry/$', views.create_registry),
    url('^api/login2/$', obtain_auth_token),
    url('^api/login/$', views.login),
    url('^api/token_test/', views.token_test),
    url('^api/signup/$', views.create_user),
    url('^$', views.test),

]
