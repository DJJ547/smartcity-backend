from .models import Camera, Iot, Drone, Incident, Congestion
from datetime import datetime, timedelta
import os
import pytz
from decimal import Decimal
from django.conf import settings


class MysqlProcessor:
    def __init__(self):
        pass

    def get_all_devices(self):
        cameras = Camera.objects.all().order_by('district')
        all_devices = {"all": {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [
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
            all_devices["all"][str(camera.district)].append(data)
            all_devices["all"]["0"].append(data)

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
            all_devices["all"][str(iot.district)].append(data)
            all_devices["all"]["0"].append(data)

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
            all_devices["all"][str(drone.dist_id)].append(data)
            all_devices["all"]["0"].append(data)
        return all_devices

    def get_all_incidents(self, time):
        if not isinstance(time, datetime):
            time = pytz.utc.localize(
                datetime.strptime(time, "%Y-%m-%d %H:%M:%S"))
        active_incidents = {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [
        ], "6": [], "7": [], "8": [], "9": [], "10": [], "11": [], "12": []}
        all_incidents = {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [
        ], "6": [], "7": [], "8": [], "9": [], "10": [], "11": [], "12": []}
        incidents = Incident.objects.all().order_by('timestamp')
        for incident in incidents:
            data = {
                'id': incident.id,
                'timestamp': incident.timestamp,
                'source': incident.source,
                'source_id': incident.source_id,
                'description': incident.description,
                'location': incident.location,
                'area': incident.area,
                'latitude': incident.latitude,
                'longitude': incident.longitude,
                'district': incident.district
            }
            all_incidents[str(incident.district)].append(data)
            all_incidents["0"].append(data)
            if timedelta(0) <= time - incident.timestamp <= timedelta(hours=1):
                active_incidents[str(incident.district)].append(data)
                active_incidents["0"].append(data)
        return {"all": all_incidents, "active": active_incidents}

    def get_all_congestions(self, time):
        if not isinstance(time, datetime):
            time = pytz.utc.localize(
                datetime.strptime(time, "%Y-%m-%d %H:%M:%S"))
        all_congestions = {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [
        ], "6": [], "7": [], "8": [], "9": [], "10": [], "11": [], "12": []}
        congestions = Incident.objects.all().order_by('timestamp')
        for congestion in congestions:
            if timedelta(0) <= time - congestion.timestamp < timedelta(minutes=5):
                data = {
                    'id': congestion.id,
                    'timestamp': congestion.timestamp,
                    'source': congestion.source,
                    'source_id': congestion.source_id,
                    'latitude': congestion.latitude,
                    'longitude': congestion.longitude,
                    'district': congestion.district
                }
                all_congestions[str(congestion.district)].append(data)
                all_congestions["0"].append(data)
        return all_congestions

    def update_all_chp_incidents_in_1min(self, time):
        if not isinstance(time, datetime):
            time = pytz.utc.localize(
                datetime.strptime(time, "%Y-%m-%d %H:%M:%S"))
        with open(os.path.join(settings.STATIC_DIRS[0], 'all_text_chp_incident_day_2024_05_27.txt'), 'r') as file:
            for line in file:
                data = line.strip().split(',')
                parsed_datetime = pytz.utc.localize(datetime.strptime(
                    data[3], "%m/%d/%Y %H:%M:%S").replace(year=time.year, month=time.month, day=time.day))
                if time.hour == parsed_datetime.hour and time.minute == parsed_datetime.minute:
                    if Incident.objects.filter(timestamp=parsed_datetime, source='chp', source_id=data[0]).exists():
                        return False
                    else:
                        if not data[9] or not data[10] or not data[11]:
                            return False
                        incident_mysql = Incident(timestamp=parsed_datetime, source='chp',
                                                  source_id=data[0], description=data[4], location=data[5], area=data[6], latitude=Decimal(float(data[9])), longitude=Decimal(float(data[10])), district=data[11])
                        incident_mysql.save()
                        return True
        return False

    def update_all_chp_incidents_from_0am_to_now(self, time):
        if not isinstance(time, datetime):
            time = pytz.utc.localize(
                datetime.strptime(time, "%Y-%m-%d %H:%M:%S"))
        with open(os.path.join(settings.STATIC_DIRS[0], 'all_text_chp_incident_day_2024_05_27.txt'), 'r') as file:
            for line in file:
                data = line.strip().split(',')
                parsed_datetime = pytz.utc.localize(datetime.strptime(
                    data[3], "%m/%d/%Y %H:%M:%S").replace(year=time.year, month=time.month, day=time.day))
                if time >= parsed_datetime:
                    if Incident.objects.filter(timestamp=parsed_datetime, source='chp', source_id=data[0]).exists():
                        continue
                    else:
                        if not data[9] or not data[10] or not data[11]:
                            continue
                        incident_mysql = Incident(timestamp=parsed_datetime, source='chp', source_id=data[0], description=data[4], location=data[5], area=data[6], latitude=Decimal(
                            float(data[9])), longitude=Decimal(float(data[10])), district=data[11])
                        print(parsed_datetime)
                        incident_mysql.save()
                else:
                    continue
        return
