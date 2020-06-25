"""Admin module"""
from django.contrib import admin
from api.models import ApiUser, DeviceType, Device, DeviceUser, Alarm, Event, GasType, WifiGlp

admin.site.register(ApiUser)
admin.site.register(DeviceType)
admin.site.register(Device)
admin.site.register(DeviceUser)
admin.site.register(Alarm)
admin.site.register(Event)
admin.site.register(GasType)
admin.site.register(WifiGlp)
