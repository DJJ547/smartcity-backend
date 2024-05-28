from .models import Camera, Iot, Drone, Incident, Congestion
from datetime import datetime, timedelta
import os
import pytz
from django.conf import settings

class MysqlProcessor:
    def __init__(self):
        pass

    def get_all_devices(self):
        cameras = Camera.objects.all().order_by('district')
        device_info = {"all": {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [
        ], "6": [], "7": [], "8": [], "9": [], "10": [], "11": [], "12": []}}
        for camera in cameras:
            data = {
                'id': camera.id,
                'index': camera.index,
                'latitude': camera.latitude,
                'longitude': camera.longitude,
                'address': camera.address,
                'dist_id': camera.district,
                'time': str(camera.time),
                'status': 'active' if camera.enabled else 'inactive',
                'type': 'camera'
            }
            device_info["all"][str(camera.district)].append(data)
            device_info["all"]["0"].append(data)

        iots = Iot.objects.all().order_by('district')
        for iot in iots:
            data = {
                'id': iot.station_id,
                'latitude': iot.latitude,
                'longitude': iot.longitude,
                'address': iot.address,
                'dist_id': iot.district,
                'status': 'active' if iot.enabled else 'inactive',
                'type': 'iot'
            }
            device_info["all"][str(iot.district)].append(data)
            device_info["all"]["0"].append(data)

        drones = Drone.objects.all().order_by('dist_id')
        for drone in drones:
            data = {
                'id': drone.id,
                'latitude': drone.latitude,
                'longitude': drone.longitude,
                'dist_id': drone.dist_id,
                'status': drone.status,
                'type': 'drone'
            }
            device_info["all"][str(drone.dist_id)].append(data)
            device_info["all"]["0"].append(data)
        return device_info
    
    def update_all_chp_incidents_in_1hour(self, time):
        if not isinstance(time, datetime):
            time = pytz.utc.localize(datetime.strptime(time, "%Y-%m-%d %H:%M:%S"))
        with open(os.path.join(settings.STATIC_DIRS[0], 'all_chp_incident_day_2024_05_23.txt'), 'r') as file:
            for line in file:
                data = line.strip().split(',')
                parsed_datetime = datetime.strptime(data[3], "%m/%d/%Y %H:%M:%S")
                if time.hour == parsed_datetime.hour:
                    if Incident.objects.filter(timestamp=parsed_datetime, source='iot', source_id=data[0]).exists():
                        return False
                    else:
                        incident_mysql = Incident(timestamp=pytz.utc.localize(parsed_datetime.replace(month=time.month, day=time.day)), source='chp', source_id=data[0])
                        incident_mysql.save()
                        return True
        return False

    # def get_all_incidents(self):
    #     incidents = Incident.objects.all().order_by('id')
    #     incident_info = {"incidents": {"0": [], "1": [], "2": [], "3": [], "4": [
    #     ], "5": [], "6": [], "7": [], "8": [], "9": [], "10": [], "11": [], "12": []}}
    #     for incident in incidents:
    #         data = {
    #             'id': incident.id,
    #             'latitude': incident.latitude,
    #             'longitude': incident.longitude,
    #             'description': incident.description,
    #             'dist_id': incident.district,
    #             'timestamp': incident.timestamp,
    #             'location': incident.location,
    #             'area': incident.area,
    #             'type': 'incident'
    #         }
    #         incident_info["incidents"][str(incident.district)].append(data)
    #         incident_info["incidents"]["0"].append(data)
    #     return incident_info