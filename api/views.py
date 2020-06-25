"""Django's views api file """
from types import SimpleNamespace
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from api.models import Event, Device, Alarm, GasType, DeviceType
from api.contracts import EventContract, RegistryContract
from api.messages import ErrorsMessages, SuccessMessages
from api.crud import Insert


class ContractException(Exception):
    """Raise contract exception"""


class ContractTypesException(Exception):
    """Raise contract types exception"""


def validate_keys(json_post, contract):
    """Validates that the json post has the same keys as the contract"""
    return json_post.keys() != contract.keys()


def validate_type_values(json_post, contract_types):
    """Validates that the values types are the as the contract"""
    return {key: (type(value)) for (key, value) in json_post.items()} != contract_types


@api_view(['GET', 'POST'])
def test(request):
    """Test if the rest server is working well"""
    success = SuccessMessages()
    return Response({"server": success.message})


@api_view(['POST'])
def create_event(request):
    """Creates an event with a POST request based in EventContract class"""
    event_contract = EventContract()
    event_fields = SimpleNamespace(**event_contract.contract_keys)
    errors = ErrorsMessages()
    success = SuccessMessages()
    insert = Insert()
    response_data = {}
    response_status = status.HTTP_201_CREATED
    try:
        json_post = request.data
        response_data["JSON_TEAM"] = json_post
        if validate_keys(json_post, event_contract.contract):
            raise ContractException()
        if validate_type_values(json_post, event_contract.contract_types):
            raise ContractTypesException()
        device = Device.objects.get(
            device_id=json_post[event_fields.device_id])
        alarm = Alarm.objects.get(alarm=json_post["alarm_level"])
        gas_type = GasType.objects.get(
            gas_type=json_post[event_fields.gas_type])
        event = Event(device=device, alarm=alarm, gas_type=gas_type)
        insert.save_model(event, json_post)
        response_data[success.message] = success.inserted(
            "Event with device: ", device.device_id)

    except KeyError:
        response_status = status.HTTP_406_NOT_ACCEPTABLE
        response_data[errors.message] = errors.invalid_post

    except Device.DoesNotExist:
        response_status = status.HTTP_404_NOT_FOUND
        response_data[errors.message] = errors.not_found("device")

    except Alarm.DoesNotExist:
        response_status = status.HTTP_404_NOT_FOUND
        response_data[errors.message] = errors.not_found("alarm_level")

    except GasType.DoesNotExist:
        response_status = status.HTTP_404_NOT_FOUND
        response_data[errors.message] = errors.not_found("gas_type")

    except ContractException:
        response_status = status.HTTP_406_NOT_ACCEPTABLE
        response_data[errors.message] = errors.json_keys

    except ContractTypesException:
        response_status = status.HTTP_406_NOT_ACCEPTABLE
        response_data[errors.message] = errors.json_types

    except IntegrityError:
        response_status = status.HTTP_406_NOT_ACCEPTABLE
        response_data[errors.message] = errors.invalid_post

    return Response(response_data, status=response_status)


@api_view(['POST'])
def create_registry(request):
    """Update device registry with the post sended based in the DeviceContract model"""
    response_data = {}
    response_status = status.HTTP_201_CREATED
    errors = ErrorsMessages()
    success = SuccessMessages()
    insert = Insert()
    registry_contract = RegistryContract()
    registry_fields = SimpleNamespace(**registry_contract.contract_keys)

    try:
        json_post = request.data
        response_data["JSON_TEAM"] = json_post
        if validate_keys(json_post, registry_contract.contract):
            raise ContractException()
        if validate_type_values(json_post, registry_contract.contract_types):
            raise ContractTypesException()
        device_type = DeviceType.objects.filter(
            name=json_post[registry_fields.device_type])
        if len(device_type) == 0:
            device_type = DeviceType(
                name=json_post[registry_fields.device_type])
            device_type.save()
        else:
            device_type = device_type[0]
        device = Device.objects.filter(
            device_id=json_post[registry_fields.device_id], serial=json_post[registry_fields.serial])
        if len(device) == 0:
            device = Device(device_type=device_type, active=True)
        else:
            device = device[0]
            device.active = True
            device.device_type = device_type
        insert.save_model(device, json_post)
        response_data[success.message] = success.inserted(
            "Device", device.device_id)

    except KeyError:
        response_data[errors.message] = errors.invalid_post

    except ContractException:
        response_status = status.HTTP_406_NOT_ACCEPTABLE
        response_data[errors.message] = errors.json_keys

    except ContractTypesException:
        response_status = status.HTTP_406_NOT_ACCEPTABLE
        response_data[errors.message] = errors.json_types

    except IntegrityError:
        response_status = status.HTTP_406_NOT_ACCEPTABLE
        response_data[errors.message] = errors.integrity_error

    return Response(response_data, status=response_status)
