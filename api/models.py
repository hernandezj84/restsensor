from django.db import models
from django.contrib.auth.models import User

class ApiUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return "{} | {} {} | {}".format(self.user.email, self.name, self.lastname, self.phone)

class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Device(models.Model):
    class Meta:
        verbose_name_plural = "devices"
    
    device_type = models.ForeignKey(Category, on_delete=models.PROTECT)
    serial_number = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return "{} | {}".format(self.device_type.name, self.serial_number)

class Event(models.Model):
    device = models.ForeignKey(Device, on_delete=models.PROTECT)
    serial = models.CharField(max_length=100)
    alarm = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return "{}-{}-{}".format(self.device, self.serial, self.alarm)

class WifiGlp(models.Model):
    device = models.ForeignKey(Device, on_delete=models.PROTECT)
    description = models.TextField()
    ppm = models.CharField(max_length=100)
    acc = models.CharField(max_length=100)
    timestamp = models.CharField(max_length=100)
    alarm = models.CharField(max_length=100)
    gas_type = models.CharField(max_length=100)

    def __str__(self):
        return "{} | {} | {} | {}".format(self.device, self.timestamp, self.alarm, self.gas_type)