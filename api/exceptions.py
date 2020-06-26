"""Module that handles all json schema and model logic exceptions"""
from functools import wraps
import os
import json
from rest_framework import status
from django.db import IntegrityError
from rest_framework.response import Response
from jsonschema import validate
from api.messages import ErrorsMessages
from api.models import Device, Alarm, GasType


MODULE_DIR = os.path.dirname(__file__)
SCHEMAS_MAP = {"create_registry": os.path.join(MODULE_DIR, "json_schemas", "registry.json"),
               "create_event": os.path.join(MODULE_DIR, "json_schemas", "event.json")}


def response_exceptions(function):
    """Creates a decorator to handle json expections"""
    @wraps(function)
    def decorated(*args, **kwargs):
        errors = ErrorsMessages()
        # TODO clear JSON_TEAM response in production
        json_data = args[0].data
        response_data = {"JSON_TEAM": json_data}
        try:
            schema = json.loads(
                open(SCHEMAS_MAP[function.__name__], "r").read())
            validate(json.dumps(json_data), schema)

            return function(*args, **kwargs)
        except KeyError:
            response_status = status.HTTP_406_NOT_ACCEPTABLE
            response_data[errors.message] = errors.invalid_post
            return Response(response_data, status=response_status)

        except Device.DoesNotExist:
            response_status = status.HTTP_404_NOT_FOUND
            response_data[errors.message] = errors.not_found("device")
            return Response(response_data, status=response_status)

        except Alarm.DoesNotExist:
            response_status = status.HTTP_404_NOT_FOUND
            response_data[errors.message] = errors.not_found("alarm_level")
            return Response(response_data, status=response_status)

        except GasType.DoesNotExist:
            response_status = status.HTTP_404_NOT_FOUND
            response_data[errors.message] = errors.not_found("gas_type")
            return Response(response_data, status=response_status)

        except IntegrityError:
            response_status = status.HTTP_406_NOT_ACCEPTABLE
            response_data[errors.message] = errors.integrity_error
            return Response(response_data, status=response_status)

        except ValueError:
            response_status = status.HTTP_406_NOT_ACCEPTABLE
            response_data[errors.message] = errors.json_keys
            return Response(response_data, status=response_status)

    return decorated
