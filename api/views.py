"""Django's views api file """
from types import SimpleNamespace
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from api.models import Event, Device, Alarm, GasType, DeviceType
from api.contracts import EventContract, RegistryContract
from api.messages import SuccessMessages
from api.crud import Insert
from api.exceptions import response_exceptions


@api_view(['GET', 'POST'])
def test(request):
    """Test if the rest server is working well"""
    success = SuccessMessages()
    return Response({"server": success.message})


@api_view(['POST'])
@response_exceptions
def create_event(request):
    """Creates an event with a POST request based in EventContract class"""
    success = SuccessMessages()
    insert = Insert()
    response_data = {}
    response_status = status.HTTP_201_CREATED

    json_post = request.data
    response_data["JSON_TEAM"] = json_post
    device = Device.objects.get(
        device_id=json_post["device_id"])
    alarm = Alarm.objects.get(alarm=json_post["alarm_level"])
    gas_type = GasType.objects.get(
        gas_type=json_post["gas_type"])
    event = Event(device=device, alarm=alarm, gas_type=gas_type)
    insert.save_model(event, json_post)
    response_data[success.message] = success.inserted(
        "Event with device: ", device.device_id)
    return Response(response_data, status=response_status)


@api_view(['POST'])
@response_exceptions
def create_registry(request):
    """Update device registry with the post sended based in the DeviceContract model"""
    response_data = {}
    response_status = status.HTTP_201_CREATED
    success = SuccessMessages()
    insert = Insert()
    json_post = request.data
    response_data["JSON_TEAM"] = json_post
    device_type = DeviceType.objects.filter(
        name=json_post["device_type"])
    if len(device_type) == 0:
        device_type = DeviceType(
            name=json_post["device_type"])
        device_type.save()
    else:
        device_type = device_type[0]
    device = Device.objects.filter(
        device_id=json_post["device_id"], serial=json_post["serial"])
    if len(device) == 0:
        device = Device(device_type=device_type, active=True)
    else:
        device = device[0]
        device.active = True
        device.device_type = device_type
    insert.save_model(device, json_post)
    response_data[success.message] = success.inserted(
        "Device", device.device_id)
    return Response(response_data, status=response_status)
