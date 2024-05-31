from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from datetime import datetime
import pandas as pd
import pytz

from .mysql import MysqlProcessor
from .mongodb import MongoDBProcessor
from smartcity_backend.iotAI import predict_average

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
def add_device(request):
    data = json.loads(request.body)
    id = data.get('id')
    if not id:
        return Response({"error": "Station ID is required"}, status=400)
    # Add device info
    mongodb = MongoDBProcessor()
    mysql = MysqlProcessor()
    deviceInfo = mongodb.get_iot_info(id)
    if not deviceInfo:
        return Response({"error": "Device not found"}, status=404)
    # return Response(deviceInfo, status=200)
    if mysql.add_device(deviceInfo):
        return Response(True, status=status.HTTP_200_OK)
    else:
        return Response(False, status=status.HTTP_409_CONFLICT)
    
@api_view(['DELETE'])
def delete_device(request):
    id = request.query_params.get('id')
    db = MysqlProcessor()
    if db.delete_device(id):
        return Response(True, status=status.HTTP_200_OK)
    else:
        return Response(False, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST', 'GET'])
def disable_device(request):
    data = json.loads(request.body)
    id = data.get('id')
    db = MysqlProcessor()
    if db.disable_or_enable_device(id):
        return Response(True, status=status.HTTP_200_OK)
    else:
        return Response(False, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_searched_devices(request):
    search_term = request.query_params.get('search')
    mongodb = MongoDBProcessor()
    devices = mongodb.search_iot_info(search_term)
    return Response(devices, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_congestions_data(request):
    current_time = pytz.utc.localize(datetime.now().replace(microsecond=0))
    mysql = MysqlProcessor()
    congestions = mysql.get_all_congestions(current_time)
    return Response({'congestions': congestions}, status=status.HTTP_200_OK)

@api_view(['POST'])
def get_flow_speed_for_one_device(request):
    predict_avg = []
    data = json.loads(request.body)
    station_id = data.get('id')
    mysql = MysqlProcessor()
    data = mysql.get_all_speed_flow_of_one_device(station_id)
    if station_id is not None:
        predict_avg = predict_average(data["predict"])
    return Response({'station_data': data["all"], 'predicted_average': predict_avg}, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def test_update_all_flow_speed_congestions_to_now(request):
    data = json.loads(request.body)
    time = data.get('time')
    mongodb = MongoDBProcessor()
    mongodb.update_all_flow_speed_congestions_from_0am_to_now(time)
    return Response({'message': 'succeed'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def test_add_iot_given_ids(request):
    data = json.loads(request.body)
    station_ids = data.get('station_ids')
    mongodb = MongoDBProcessor()
    mongodb.test_add_iots_given_list(station_ids)
    return Response({'message': 'succeed'}, status=status.HTTP_200_OK)
