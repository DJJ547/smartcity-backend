from queue import Queue
import cv2
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseNotAllowed, JsonResponse, StreamingHttpResponse

from smartcity_backend.detection import detect
from .mysql import MysqlProcessor
from .mongodb import MongoDBProcessor

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view

from rest_framework import status
from rest_framework.response import Response


from data_backend.models import Drone, Incident

import json

streaming = True

@csrf_exempt
def addDevice(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        altitude = data.get('altitude')
        timestamp = data.get('timestamp')
        dist_id = data.get('dist_id')
        status = data.get('status')
        if Drone.objects.filter(id=id).exists():
            print("device already exists")
            return HttpResponse(json.dumps('device address already exist'), status=409)
        else:
            new_device = Drone(id=id, latitude=latitude, longitude=longitude, altitude=altitude, timestamp=timestamp, dist_id=dist_id, status = status)
            new_device.save()
            print('device added')
            return HttpResponse(json.dumps('device succeed'), status=200)
    else:
        return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def UpdateDeviceInfo(request):
        if request.method == 'PUT':
            data = json.loads(request.body)
            id = data.get('update_id')
            latitude = data.get('update_latitude')
            longitude = data.get('update_longitude')
            altitude = data.get('update_altitude')
            timestamp = data.get('update_timestamp')
            dist_id = data.get('update_dist_id')
            status = data.get('update_status')

            try:
                device = Drone.objects.get(id=id)
                device.latitude = latitude
                device.longitude = longitude
                device.altitude = altitude
                device.timestamp = timestamp
                device.dist_id = dist_id
                device.enabled = status
                device.save()
                print('Device updated successfully')
                return HttpResponse(json.dumps('Device updated successfully'), status=200)
            except Drone.DoesNotExist:
                print("Device does not exist")
                return HttpResponse(json.dumps('Device does not exist'), status=404)
        else:
            return HttpResponseNotAllowed(['PUT'])
        
@csrf_exempt
def getDeviceInfo(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        try:
            device = Drone.objects.get(id=id)
            device_data = {
                'id': device.id,
                'latitude': device.latitude,
                'longitude': device.longitude,
                'altitude': device.altitude,
                'timestamp': device.timestamp,
                'dist_id': device.dist_id,
                'status': device.enabled
            }
            return JsonResponse(device_data)
        except Drone.DoesNotExist:
            return JsonResponse({'error': 'Device not found'}, status=404)
            
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def deleteDevice(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        id = data.get('id')
        if id is None:
            return HttpResponse('Drone ID not provided', status=400)

        try:
            device = Drone.objects.get(id=id)
            device.delete()
            print('device deleted')
            return HttpResponse('Device deleted', status=200)
        except Drone.DoesNotExist:
            return HttpResponse('Device not found', status=404)
    else:
        return HttpResponseNotAllowed(['DELETE'])
    
@csrf_exempt 
def get_video_urls(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        print("Received id:", id)
        mongodb = MongoDBProcessor()
        try:
            deviceInfo = mongodb.get_drone_info(id)
            device_data = {
                'id': id,
                'videourl' : deviceInfo['video_url']
            }
            print(device_data)
            return JsonResponse(device_data)
        except Drone.DoesNotExist:
            return JsonResponse({'error': 'video url not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

@csrf_exempt 
def getAllDevices(request):
    if request.method == 'GET':
        db = MysqlProcessor()
        devices = db.get_all_devices()
        #print("getAllDevices",devices)
        return JsonResponse(devices, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
        
def updateImage(request):
    id = "1"
    # update image url
    mongodb = MongoDBProcessor()
    image_url = mongodb.get_image_url(id)
    db = MysqlProcessor()
    if db.updateImage(id, image_url):
        return HttpResponse('Image updated')
    else:
        return HttpResponse('Device not found')

def disableDevice(request):
    id = "1"
    # disable device
    db = MysqlProcessor()
    if db.disable_device(id):
        return HttpResponse('Device disabled')
    else:
        return HttpResponse('Device not found')

# added from yifu's code all 3 functions
    
@csrf_exempt
def searchedDevice(request):
    if request.method == 'GET':
        search_term = request.query_params.get('search')
        # search device
        db = MongoDBProcessor()
        result = db.search_device(search_term)
        return JsonResponse(result, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def GetAllIncidences(request):
    # get all incidents
    db = MysqlProcessor()
    incidents = db.get_all_incidents()
    return Response(incidents, status=status.HTTP_200_OK)        

@api_view(['GET'])
def streamVideo(request):
    id = request.query_params.get('id')
    print("Received id for stream video:", id)
    mongodb = MongoDBProcessor()
    deviceInfo = mongodb.get_drone_info(id)
    device_data = {
        'id': id,
        'videourl' : deviceInfo['video_url'],
        'latitude' : deviceInfo['latitude'],
        'longitude': deviceInfo['longitude'],
        'dist_id' : deviceInfo['dist_id']
    }
    print("stream video", device_data)
    print(deviceInfo['video_url'])
    # get video stream
    # Open the video file
    BUFFER_SIZE = 30
    cap = cv2.VideoCapture(deviceInfo['video_url'])
    print("streamvideo from cap cv2",cap)
    # The buffer for storing frames
    buffer = Queue(maxsize=BUFFER_SIZE)
    print(streaming)
    def generate():
        while streaming:
            ret, frame = cap.read()
            if ret:
                # frame = cv2.resize(frame, (640, 360))
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
                    if db.add_incidents(deviceInfo['latitude'], deviceInfo['longitude'], 'incident', deviceInfo['dist_id']) == False:
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