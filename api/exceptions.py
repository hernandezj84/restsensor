"""Module that handles all json schema and model logic exceptions"""
from functools import wraps
import re
import os
import json
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from jsonschema import validate
from api.messages import ErrorsMessages
from api.models import Device, Alarm, GasType

EMAIL_PATTERN = "^\w+@[a-zA-Z_]+?.[a-zA-Z]{2,3}$"
MODULE_DIR = os.path.dirname(__file__)
SCHEMAS_MAP = {"create_registry": os.path.join(MODULE_DIR, "json_schemas", "registry.json"),
               "create_event": os.path.join(MODULE_DIR, "json_schemas", "event.json"),
               "create_user": os.path.join(MODULE_DIR, "json_schemas", "signup.json")}


class EmailException(Exception):
    """Raise contract exception"""


def response_exceptions(function):
    """Creates a decorator to handle json expections"""
    @wraps(function)
    def decorated(*args, **kwargs):
        errors = ErrorsMessages()
        json_data = args[0].data
        response_data = {"JSON_TEAM": json_data}
        try:
            schema = json.loads(
                open(SCHEMAS_MAP[function.__name__], "r").read())
            validate(json.dumps(json_data), schema)
            if "user_email" in json_data:
                if not re.search(EMAIL_PATTERN, json_data["user_email"]):
                    raise EmailException('The email is not correct')

            return function(*args, **kwargs)
        except KeyError as error:
            response_status = status.HTTP_406_NOT_ACCEPTABLE
            response_data[errors.message] = str(error)
            return Response(response_data, status=response_status)

        except EmailException as error:
            response_status = status.HTTP_406_NOT_ACCEPTABLE
            response_data[errors.message] = str(error)
            return Response(response_data, status=response_status)

        except Device.DoesNotExist as error:
            response_status = status.HTTP_404_NOT_FOUND
            response_data[errors.message] = str(error)
            return Response(response_data, status=response_status)

        except Alarm.DoesNotExist as error:
            response_status = status.HTTP_404_NOT_FOUND
            response_data[errors.message] = str(error)
            return Response(response_data, status=response_status)

        except GasType.DoesNotExist as error:
            response_status = status.HTTP_404_NOT_FOUND
            response_data[errors.message] = str(error)
            return Response(response_data, status=response_status)

        except IntegrityError as error:
            response_status = status.HTTP_406_NOT_ACCEPTABLE
            response_data[errors.message] = str(error)
            return Response(response_data, status=response_status)

        except ValueError as error:
            response_status = status.HTTP_406_NOT_ACCEPTABLE
            response_data[errors.message] = str(error)
            return Response(response_data, status=response_status)

    return decorated
