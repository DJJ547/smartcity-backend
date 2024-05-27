from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json

from .mysql import MysqlProcessor
from .mongodb import MongoDBProcessor

@api_view(['GET'])
def get_all_data(request):
    mysql = MysqlProcessor()
    devices = mysql.get_all_devices()
    return Response({'devices': devices}, status=status.HTTP_200_OK)

@api_view(['POST'])
def update_all_speed(request):
    data = json.loads(request.body)
    time = data.get('time')
    mongodb = MongoDBProcessor()
    all_speed = mongodb.update_all_speed_in_5min(time)
    return Response({'speed': all_speed}, status=status.HTTP_200_OK)
