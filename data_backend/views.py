from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .mysql import MysqlProcessor
from datetime import datetime
import json
import pytz
    
@api_view(['GET'])
def get_all_devices_data(request):
    mysql = MysqlProcessor()
    devices = mysql.get_all_devices()
    return Response({'devices': devices}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_incidents_data(request):
    current_time = pytz.utc.localize(datetime.now().replace(microsecond=0))
    mysql = MysqlProcessor()
    incidents = mysql.get_all_incidents(current_time)
    return Response({'active': incidents["active"], 'all': incidents["all"]}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_congestions_data(request):
    current_time = pytz.utc.localize(datetime.now().replace(microsecond=0))
    mysql = MysqlProcessor()
    congestions = mysql.get_all_congestions(current_time)
    return Response({'congestions': congestions}, status=status.HTTP_200_OK)

# testing only
@api_view(['POST'])
def test_get_all_incidents(request):
    data = json.loads(request.body)
    time = data.get('time')
    mysql = MysqlProcessor()
    incidents = mysql.get_all_incidents(time)
    return Response({'incidents': incidents}, status=status.HTTP_200_OK)

# testing only
@api_view(['POST'])
def test_update_incidents_in_1hour(request):
    data = json.loads(request.body)
    time = data.get('time')
    mysql = MysqlProcessor()
    mysql.update_all_chp_incidents_in_1hour(time)
    return Response({'message': 'succeed'}, status=status.HTTP_200_OK)

# testing only
@api_view(['POST'])
def test_update_incidents_from_0am_to_now(request):
    data = json.loads(request.body)
    time = data.get('time')
    mysql = MysqlProcessor()
    mysql.update_all_chp_incidents_from_0am_to_now(time)
    return Response({'message': 'succeed'}, status=status.HTTP_200_OK)
