from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json

from .mysql import MysqlProcessor

@api_view(['POST'])
def login(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    mysql = MysqlProcessor()
    res = mysql.authenticate_user(email, password)
    if res['result']:
        return Response({
            'message': res['message'],
            'email': res['user'].email,
            'firstname': res['user'].first_name,
            'lastname': res['user'].last_name,
            'is_agent':res['user'].is_staff,
            'token': res['token']
        }, status=status.HTTP_200_OK)
    else:
        return Response({'message': res['message']}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def signup(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    mysql = MysqlProcessor()
    res = mysql.register_user(email, password, firstname, lastname)
    if res['result']:
        return Response({'message': res}, status=status.HTTP_200_OK)
    else:
        return Response({'message': res}, status=status.HTTP_409_CONFLICT)
    