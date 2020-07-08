"""Module that handles all json schema and model logic exceptions"""
from functools import wraps
import re
import os
import json
from django.db import IntegrityError
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from jsonschema import validate
from api.messages import ErrorsMessages
from api.models import Device, Alarm, GasType, ApiUser

EMAIL_PATTERN = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
MODULE_DIR = os.path.dirname(__file__)
SCHEMAS_MAP = {"create_registry": os.path.join(MODULE_DIR, "json_schemas", "registry.json"),
               "create_event": os.path.join(MODULE_DIR, "json_schemas", "event.json"),
               "create_user": os.path.join(MODULE_DIR, "json_schemas", "signup.json"),
               "login": os.path.join(MODULE_DIR, "json_schemas", "login.json")}


class EmailException(Exception):
    """Raise contract exception"""


class UserNameException(Exception):
    """Raise username exception"""


class EmailNotFound(Exception):
    """Raise email not found exception"""


def response_exceptions(function):
    """Creates a decorator to handle json expections"""
    @wraps(function)
    def decorated(*args, **kwargs):
        errors = ErrorsMessages()
        json_data = args[0].data
        response_data = {"JSON_TEAM": json_data}
        try:
            if function.__name__ != "token_test":
                schema = json.loads(
                    open(SCHEMAS_MAP[function.__name__], "r").read())
                validate(json.dumps(json_data), schema)
                if function.__name__ == "create_user":
                    if not re.search(EMAIL_PATTERN, json_data["user_email"]):
                        raise EmailException('The email is not correct')

                    if ApiUser.objects.filter(user_name=json_data["user_name"]).exists():
                        raise UserNameException('user_name already exists')
                if function.__name__ == "login":
                    if not authenticate(username=json_data["user_email"], password=json_data["password"]):
                        raise EmailNotFound(
                            'user_email not found or invalid password')

            if function.__name__ == "token_test":
                Token.objects.get(key=args[0].auth)

            return function(*args, **kwargs)
        except KeyError as error:
            response_status = status.HTTP_406_NOT_ACCEPTABLE
            response_data[errors.message] = str(error)
            return Response(response_data, status=response_status)

        except EmailException as error:
            response_status = status.HTTP_406_NOT_ACCEPTABLE
            response_data[errors.message] = str(error)
            return Response(response_data, status=response_status)

        except EmailNotFound as error:
            response_status = status.HTTP_406_NOT_ACCEPTABLE
            response_data[errors.message] = str(error)
            return Response(response_data, status=response_status)

        except UserNameException as error:
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
