import json
from data_backend.models import Iot, Congestion
from .models import Station_Speed
from datetime import datetime, timedelta
import pytz


class MysqlProcessor:
    def __init__(self):
        pass

    def add_device(self, device_info):
        if Iot.objects.filter(station_id=device_info['station_id']).exists():
            return False
        else:
            device_mysql = Iot(
                station_id=device_info['station_id'],
                address=device_info['address'],
                latitude=device_info['latitude'],
                longitude=device_info['longitude'],
                district=device_info['district'],
                hourlySpeed=device_info['hourlySpeed']
            )
            device_mysql.save()
            return True

    def update_device_info(self, device_info):
        if Iot.objects.filter(index=device_info['index']).exists():
            device_mysql = Iot.objects.get(index=device_info['index'])
            device_mysql.latitude = device_info['latitude']
            device_mysql.longitude = device_info['longitude']
            device_mysql.image_url = device_info['image_url']
            device_mysql.address = device_info['address']
            device_mysql.district = device_info['district']
            device_mysql.time = device_info['time']
            device_mysql.save()
        else:
            device_mysql = Iot(index=device_info['index'], latitude=device_info['latitude'], longitude=device_info['longitude'],
                               image_url=device_info['image_url'], address=device_info['address'], time=device_info['time'], district=device_info['district'])
            device_mysql.save()

    def get_device_info(self, request_index):
        if Iot.objects.filter(index=request_index).exists():
            device = Iot.objects.get(index=request_index)
            device_info = {
                'id': device.station_id,
                'latitude': device.latitude,
                'longitude': device.longitude,
                'freeway': device.freeway,
                'direction': device.direction,
                'district': device.district,
                # Parse hourlySpeed from string to list
                'hourlySpeed': json.loads(device.hourlySpeed),
            }
            return device_info
        else:
            return None

    def delete_device(self, id):
        print(id)
        if Iot.objects.filter(station_id=id).exists():
            device_mysql = Iot.objects.get(station_id=id)
            device_mysql.delete()
            return True
        else:
            return False

    def updateImage(self, request_index, image_url):
        if Iot.objects.filter(index=request_index).exists():
            device_mysql = Iot.objects.get(index=request_index)
            device_mysql.image_url = image_url
            device_mysql.save()
            return True
        else:
            return False

    def disable_or_enable_device(self, request_index):
        if Iot.objects.filter(station_id=request_index).exists():
            device_mysql = Iot.objects.get(station_id=request_index)
            device_mysql.enabled = not device_mysql.enabled
            device_mysql.save()
            return True
        else:
            return False

    def get_all_devices(self):
        devices = Iot.objects.all().order_by('district')
        all_devices = {"iots": {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [
        ], "6": [], "7": [], "8": [], "9": [], "10": [], "11": [], "12": []}}
        for device in devices:
            data = {
                'id': device.station_id,
                'latitude': device.latitude,
                'longitude': device.longitude,
                'address': device.freeway + " " + device.direction + "," + device.city + "," + device.county,
                'dist_id': device.district,
                'status': 'active' if device.enabled else 'inactive',
                'type': 'iot'
            }
            all_devices["iots"][str(device.district)].append(data)
            all_devices["iots"]["0"].append(data)
        return all_devices

    def get_all_congestions(self, time):
        if not isinstance(time, datetime):
            time = pytz.utc.localize(
                datetime.strptime(time, "%Y-%m-%d %H:%M:%S"))
        active_congestions = {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [
        ], "6": [], "7": [], "8": [], "9": [], "10": [], "11": [], "12": []}
        all_congestions = {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [
        ], "6": [], "7": [], "8": [], "9": [], "10": [], "11": [], "12": []}
        congestions = Congestion.objects.all().order_by('timestamp')
        for congestion in congestions:
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
            if timedelta(0) <= time - congestion.timestamp < timedelta(minutes=5):
                active_congestions[str(congestion.district)].append(data)
                active_congestions["0"].append(data)
        return {"all": all_congestions, "active": active_congestions}

    def get_all_speed_flow_of_one_device(self, id):
        all_data = []
        if Station_Speed.objects.filter(station_id=id).exists():
            all_speed_flow = Station_Speed.objects.filter(station_id=id).order_by("timestamp")
            for speed_flow in all_speed_flow:
                data = {
                    'id': speed_flow.id,
                    'timestamp': speed_flow.timestamp,
                    'speed': speed_flow.speed,
                    'flow': speed_flow.flow,
                    'station_id': speed_flow.station_id
                }
                all_data.append(data)
        return all_data
