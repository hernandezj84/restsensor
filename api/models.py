"""Django's api model file"""
from django.db import models
from django.contrib.auth.models import User


class ApiUser(models.Model):
    """Model inheriting from user class. Gives more accurate fields for the user"""
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return "{} | {} {} | {}".format(self.user, self.name, self.lastname, self.phone)


class Category(models.Model):
    """Model of the device_type category"""
    class Meta:
        verbose_name_plural = "categories"
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Device(models.Model):
    """Model of the device"""
    class Meta:
        verbose_name_plural = "devices"
    device_id = models.CharField(max_length=20, unique=True)
    device_type = models.ForeignKey(Category, on_delete=models.PROTECT)
    serial = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return "{} | {}".format(self.device_id, self.device_type)


class DeviceUser(models.Model):
    """Model that combines the Device and the Django's User model"""
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    device = models.ForeignKey(Device, on_delete=models.PROTECT)

    def __str__(self):
        return "{} | {}".format(self.user, self.device)


class Alarm(models.Model):
    """Model that defines the type of the alarms"""
    alarm = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=25)

    def __str__(self):
        return "{} | {}".format(self.alarm, self.description)


class Event(models.Model):
    """Model that defines a device's event"""
    device = models.ForeignKey(Device, on_delete=models.PROTECT)
    alarm = models.ForeignKey(Alarm, on_delete=models.PROTECT)
    acc_time = models.CharField(max_length=100)
    timestamp = models.CharField(max_length=100)
    concent_gas = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    def __str__(self):
        return "{}-{}-{}-{}".format(self.device, self.alarm, self.timestamp, self.status)


class GasType(models.Model):
    """Model that defines the category or the types of gases for the project"""
    gas_type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.gas_type


class WifiGlp(models.Model):
    """Model that defines a special event. When this object is saved
    it will trigger a document to Firebase"""
    device = models.ForeignKey(Device, on_delete=models.PROTECT)
    concent_gas = models.CharField(max_length=100)
    acc_time = models.CharField(max_length=100)
    timestamp = models.CharField(max_length=100)
    alarm = models.ForeignKey(Alarm, on_delete=models.PROTECT)
    gas_type = models.ForeignKey(GasType, on_delete=models.PROTECT)

    def __str__(self):
        return "{} | {} | {} | {}".format(self.device, self.timestamp, self.alarm, self.gas_type)
