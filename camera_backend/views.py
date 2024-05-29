from django.shortcuts import render, HttpResponse, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import StreamingHttpResponse
from .mongodb import MongoDBProcessor
from .mysql import MysqlProcessor
import json
from .detection import detect
import cv2
import numpy as np
from queue import Queue

streaming = True

@api_view(['POST'])
def addDevice(request):
    request_id = int(request.query_params.get('id'))
    # add device info
    mongodb = MongoDBProcessor()
    mysql = MysqlProcessor()
    deviceInfo = mongodb.get_camera_info(request_id)
    if mysql.add_device(deviceInfo):
        return Response('Device added', status=status.HTTP_200_OK)
    else:
        return Response('Device already exists', status=status.HTTP_409_CONFLICT)

@api_view(['GET'])
def GetALLDevices(request):
    # get all devices info
    db = MysqlProcessor()
    devices = db.get_all_devices()
    global streaming
    streaming = True
    return Response(devices, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def deleteDevice(request):
    request_id = request.query_params.get('id')
    # delete device info
    db = MysqlProcessor()
    if db.delete_device(request_id):
        return Response('Device deleted', status=status.HTTP_200_OK)
    else:
        return Response('Device not found', status=status.HTTP_404_NOT_FOUND)

@api_view(['POST', 'GET'])
def disableDevice(request):
    request_id = request.query_params.get('id')
    # disable device
    db = MysqlProcessor()
    if db.disable_or_enable_device(request_id):
        return Response('Status switched', status=status.HTTP_200_OK)
    else:
        return Response('Device not found', status=status.HTTP_404_NOT_FOUND)
        
@api_view(['GET'])
def searchedDevice(request):
    search_term = request.query_params.get('search')
    # search device
    db = MongoDBProcessor()
    result = db.search_device(search_term)
    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
def GetAllIncidences(request):
    # get all incidents
    db = MysqlProcessor()
    incidents = db.get_all_incidents()
    return Response(incidents, status=status.HTTP_200_OK)

@api_view(['GET'])
def streamVideo(request):
    request_url = request.query_params.get('url')
    latitude = request.query_params.get('latitude')
    longitude = request.query_params.get('longitude')
    district = request.query_params.get('district')

    # get video stream
    # Open the video file
    BUFFER_SIZE = 30
    cap = cv2.VideoCapture(request_url)
    # The buffer for storing frames
    buffer = Queue(maxsize=BUFFER_SIZE)
    print(streaming)
    def generate():
        while streaming:
            ret, frame = cap.read()
            if ret:
                #frame = cv2.resize(frame, (640, 360))
                results = detect(frame, incident=False)
                results_incident = detect(frame, incident=True)
                # Draw rectangle
                for result in results:
                    position = [int(p) for p in result['position']]
                    cv2.rectangle(frame, (position[0], position[1]), (position[2], position[3]), (0, 255, 0), 2)
                    cv2.putText(frame, result['label'], (position[0], position[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2, cv2.LINE_AA)
                
                for result in results_incident:
                    position = [int(p) for p in result['position']]
                    cv2.rectangle(frame, (position[0], position[1]), (position[2], position[3]), (0, 0, 255), 2)
                    cv2.putText(frame, result['label'], (position[0], position[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2, cv2.LINE_AA)

                # Add the incident to the database
                if len(results_incident) > 0:
                    db = MysqlProcessor()
                    if db.add_incidents(latitude, longitude, 'incident', district) == False:
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