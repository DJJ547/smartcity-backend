from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json

from .mysql import MysqlProcessor
from .mongodb import MongoDBProcessor

@api_view(['GET'])
def get_all_devices_data(request):
    mysql = MysqlProcessor()
    devices = mysql.get_all_devices()
    return Response({'devices': devices}, status=status.HTTP_200_OK)

@api_view(['POST'])
def test_update_all_flow_speed_congestions(request):
    data = json.loads(request.body)
    time = data.get('time')
    mongodb = MongoDBProcessor()
    mongodb.update_all_flow_speed_congestion_in_5min(time)
    return Response({'message': 'succeed'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def test_update_all_flow_speed_congestions_to_now(request):
    data = json.loads(request.body)
    time = data.get('time')
    mongodb = MongoDBProcessor()
    mongodb.update_all_flow_speed_congestions_from_0am_to_now(time)
    return Response({'message': 'succeed'}, status=status.HTTP_200_OK)

