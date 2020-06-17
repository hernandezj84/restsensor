from django.contrib import admin
from api.models import ApiUser, Category, Device, Event, WifiGlp

admin.site.register(ApiUser)
admin.site.register(Category)
admin.site.register(Device)
admin.site.register(Event)
admin.site.register(WifiGlp)
