from django.shortcuts import render, HttpResponse, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import StreamingHttpResponse
from .mongodb import MongoDBProcessor
from .mysql import MysqlProcessor
import json
from smartcity_backend.detection import detect
import cv2
import numpy as np
from queue import Queue
import pytz
from datetime import datetime
import logging

streaming = True
def draw_results(frame, results, color):
    for result in results:
        position = [int(p) for p in result['position']]
        cv2.rectangle(frame, (position[0], position[1]),
                      (position[2], position[3]), color, 2)
        cv2.putText(frame, result['label'], (position[0], position[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 2, cv2.LINE_AA)
db = MysqlProcessor()

@api_view(['POST'])
def addDevice(request):
    request_id = int(request.query_params.get('id'))
    # add device info
    mongodb = MongoDBProcessor()
    deviceInfo = mongodb.get_drone_info(request_id)
    if db.add_device(deviceInfo):
        return Response(True, status=status.HTTP_200_OK)
    else:
        return Response(False, status=status.HTTP_409_CONFLICT)

@api_view(['GET'])
def GetALLDevices(request):
    # get all devices info
    devices = db.get_all_devices()
    global streaming
    streaming = True
    return Response(devices, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def deleteDevice(request):
    request_id = request.query_params.get('id')
    if db.delete_device(request_id):
        return Response(True, status=status.HTTP_200_OK)
    else:
        return Response(False, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST', 'GET'])
def disableDevice(request):
    request_id = request.query_params.get('id')
    if db.disable_or_enable_device(request_id):
        return Response(True, status=status.HTTP_200_OK)
    else:
        return Response(False, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['GET'])
def searchedDevice(request):
    search_term = request.query_params.get('search')
    # search device
    mongodb = MongoDBProcessor()
    result = mongodb.search_device(search_term)
    print(result)
    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
def GetAllIncidences(request):
    current_time = pytz.utc.localize(datetime.now().replace(microsecond=0))
    # get all incidents
    incidents = db.get_all_incidents(current_time)
    return Response(incidents, status=status.HTTP_200_OK)

@api_view(['GET'])
def streamVideo(request):
    id = request.query_params.get('id')
    print("Received id for stream video:", id)
    mongodb = MongoDBProcessor()
    deviceInfo = mongodb.get_drone_info(int(id))
    """ device_data = {
        'id': id,
        'videourl' : deviceInfo['video_url'],
        'latitude' : deviceInfo['latitude'],
        'longitude': deviceInfo['longitude'],
        'dist_id' : deviceInfo['dist_id']
    }
    print("stream video", device_data)
    print(deviceInfo['video_url']) """
    # get video stream
    # Open the video file
    BUFFER_SIZE = 30
    cap = cv2.VideoCapture(deviceInfo['video_url'])

    # The buffer for storing frames
    buffer = Queue(maxsize=BUFFER_SIZE)
    print(streaming)
    def generate():
        while streaming:
            ret, frame = cap.read()
            if ret:
                try:
                    results = detect(frame, incident=False)
                    results_incident = detect(frame, incident=True)
                except Exception as e:
                    logging.error(f"Detection failed: {e}")
                    return
                
                draw_results(frame, results, (0, 255, 0))
                draw_results(frame, results_incident, (0, 0, 255))

                # Add the incident to the database
                if len(results_incident) > 0:
                    if db.add_incidents(deviceInfo['latitude'], deviceInfo['longitude'], 'drone', deviceInfo['dist_id']) == False:
                        print('Incident already exists')
                    else:
                        print('Incident added')

                # Display total number of cars
                cv2.putText(frame, f'Car: {len(results)}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(frame, f'Incident: {len(results_incident)}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

                # Encode the frame as JPEG
                ret, jpeg = cv2.imencode('.jpeg', frame)
                if ret:
                    # Add the frame to the buffer
                    buffer.put(jpeg.tobytes())

                if buffer:
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + buffer.get() + b'\r\n\r\n')
    
    return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')

@api_view(['GET'])
def stopStream(request):
    global streaming
    streaming = False
    return Response('Stream stopped', status=status.HTTP_200_OK)