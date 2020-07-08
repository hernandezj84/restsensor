"""Django's views api file """
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from api.messages import SuccessMessages
from api.crud import Crud
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
    response_data = {}
    json_post = request.data
    success = SuccessMessages()
    crud = Crud()
    event = crud.save_event(json_post)
    response_status = status.HTTP_201_CREATED
    response_data[success.message] = success.inserted(
        "Event with device: ", event.device.device_id)
    return Response(response_data, status=response_status)


@api_view(['POST'])
@response_exceptions
def create_registry(request):
    """Update device registry with the post sended based in the DeviceContract model"""
    json_post = request.data
    response_data = {}
    response_status = status.HTTP_201_CREATED
    success = SuccessMessages()
    crud = Crud()
    device = crud.save_registry(json_post)
    response_data[success.message] = success.inserted(
        "Device", device.device_id)
    return Response(response_data, status=response_status)


@api_view(['POST'])
@response_exceptions
def create_user(request):
    """Create a user on django database"""
    json_post = request.data
    response_data = {}
    response_status = status.HTTP_201_CREATED
    token = Crud.save_user(json_post)
    response_data["token"] = token
    return Response(response_data, status=response_status)


@api_view(['POST'])
@response_exceptions
def login(request):
    """Response with token"""
    json_post = request.data
    response_data = {}
    response_status = status.HTTP_200_OK
    token = Crud.login(json_post)
    response_data["token"] = token
    return Response(response_data, status=response_status)
