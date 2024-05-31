from data_backend.models import Drone, Incident
from django.utils import timezone
from decimal import Decimal
from datetime import datetime, timedelta


class MysqlProcessor:
    def __init__(self):
        pass

    def add_device(self, device_info):
        if device_info is None:
            return False

        if Drone.objects.filter(id=device_info['id']).exists():
            return False
        else:
            device_mysql = Drone(id=device_info['id'], latitude=device_info['latitude'], longitude=device_info['longitude'], altitude=device_info['altitude'],timestamp=device_info['time'], dist_id=device_info['dist_id'], video_url=device_info['video_url'])
            device_mysql.save()
            return True

    def delete_device(self, id):
        if Drone.objects.filter(id=id).exists():
            device_mysql = Drone.objects.get(id=id)
            device_mysql.delete()
            return True
        else:
            return False

    def disable_or_enable_device(self, id):
        if Drone.objects.filter(id=id).exists():
            device_mysql = Drone.objects.get(id=id)
            device_mysql.enabled = not device_mysql.enabled
            device_mysql.save()
            return True
        else:
            return False

    def get_all_devices(self):
        devices = Drone.objects.all().order_by('id')
        device_info = {"drones": {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [
        ], "6": [], "7": [], "8": [], "9": [], "10": [], "11": [], "12": []}}
        for device in devices:
            data = {
                'id': device.id,
                'latitude': device.latitude,
                'longitude': device.longitude,
                'time': str(device.timestamp),
                'dist_id': device.dist_id,
                'status': 'active' if device.enabled else 'inactive',
                'video_url': device.video_url
            }
            device_info["drones"][str(device.dist_id)].append(data)
            device_info["drones"]["0"].append(data)

        return device_info

    # add a new incident, if theres one already, update the timestamp instead
    def add_incidents(self, lat, lon, Type, district):
        # lat decimal with 5 decimal place
        lat = Decimal(lat).quantize(Decimal('1.00000'))
        # lon decimal with 5 decimal place
        lon = Decimal(lon).quantize(Decimal('1.00000'))

        if Incident.objects.filter(latitude=lat, longitude=lon, district=district).exists():
            incident = Incident.objects.get(
                latitude=lat, longitude=lon, district=district)
            incident.timestamp = timezone.now()
            incident.save()
            return False
        else:
            incident = Incident(latitude=lat, longitude=lon,
                                source=Type, district=district)
            incident.save()
        return True

    def get_all_incidents(self, time):
        incidents = Incident.objects.all()
        active_incident = {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [
        ], "6": [], "7": [], "8": [], "9": [], "10": [], "11": [], "12": []}
        for incident in incidents:
            data = {
                'id': incident.id,
                'timestamp': str(incident.timestamp),
                'source_id': incident.source_id,
                'description': incident.description,
                'location': incident.location,
                'area': incident.area,
                'latitude': incident.latitude,
                'longitude': incident.longitude,
                'district': incident.district
            }
            if incident.source == 'drone' and timedelta(0) <= time - incident.timestamp <= timedelta(hours=1):
                active_incident[str(incident.district)].append(data)
                active_incident["0"].append(data)
        return active_incident


def test():
    mysql = MysqlProcessor()
    lat = 37.7343
    lon = -122.41
    Type = 'incident'
    result = mysql.add_incidents(lat, lon, Type)
    if result:
        print('Incident added successfully')
    else:
        print('Incident already exists')
