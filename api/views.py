"""Django's views api file """
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from api.models import Event, Device, Alarm, GasType
from api.contracts import ContractEvent
from api.messages import ErrorsMessages, SuccessMessages
from api.crud import Insert
from types import SimpleNamespace


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
    c_event = ContractEvent()
    c_fields = SimpleNamespace(**c_event.contract_keys)
    errors = ErrorsMessages()
    success = SuccessMessages()
    insert = Insert()
    data = {}
    response_status = status.HTTP_201_CREATED
    try:
        json_post = request.data
        print(json_post)
        if validate_keys(json_post, c_event.contract):
            raise ContractException()
        if validate_type_values(json_post, c_event.contract_types):
            raise ContractTypesException()
        device = Device.objects.get(device_id=json_post[c_fields.device_id])
        alarm = Alarm.objects.get(alarm=json_post[c_fields.alarm_level])
        gas_type = GasType.objects.get(gas_type=json_post[c_fields.gas_type])
        event = Event(device=device, alarm=alarm, gas_type=gas_type)
        insert.save_model(event, json_post)
        data[success.message] = success.inserted("Event with device: ", device.device_id)

    except KeyError:
        response_status = status.HTTP_406_NOT_ACCEPTABLE
        data[errors.message] = errors.invalid_post

    except Device.DoesNotExist:
        response_status = status.HTTP_404_NOT_FOUND
        data[errors.message] = errors.not_found("device")

    except Alarm.DoesNotExist:
        response_status = status.HTTP_404_NOT_FOUND
        data[errors.message] = errors.not_found("alarm")

    except GasType.DoesNotExist:
        response_status = status.HTTP_404_NOT_FOUND
        data[errors.message] = errors.not_found("alarm")

    except ContractException:
        response_status = status.HTTP_406_NOT_ACCEPTABLE
        data[errors.message] = errors.json_keys

    except ContractTypesException:
        response_status = status.HTTP_406_NOT_ACCEPTABLE
        data[errors.message] = errors.json_types

    except IntegrityError:
        response_status = status.HTTP_406_NOT_ACCEPTABLE
        data[errors.message] = errors.invalid_post

    return Response(data, status=response_status)
