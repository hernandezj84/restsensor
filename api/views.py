from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET'])
def test(request):
    data = {"message": "hello world from api"}
    return Response(data)