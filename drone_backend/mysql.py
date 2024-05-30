from data_backend.models import Drone, Incident
from django.utils import timezone
from decimal import Decimal

class MysqlProcessor:
    def __init__(self):
        pass

    def add_device(self, device_info):
        if Drone.objects.filter(id=device_info['id']).exists():
            return False
        else:
            device_mysql = Drone(id=device_info['id'], latitude=device_info['latitude'], longitude=device_info['longitude'], altitude=device_info['altitude'], timestamp=device_info['timestamp'], dist_id=device_info['dist_id'], video_url=device_info['video_url'])
            device_mysql.save()

    def update_device_info(self, device_info):
        if Drone.objects.filter(id=device_info['id']).exists():
            device_mysql = Drone.objects.get(id=device_info['id'])
            device_mysql.latitude = device_info['latitude']
            device_mysql.longitude = device_info['longitude']
            device_mysql.altitude = device_info['altitude']       
            device_mysql.dist_id = device_info['dist_id']
            device_mysql.timestamp = device_info['timestamp']
            device_mysql.video_url = device_info['video_url']
            device_mysql.save()
        else:
            device_mysql = Drone(id=device_info['id'], latitude=device_info['latitude'], longitude=device_info['longitude'], altitude=device_info['altitude'], timestamp=device_info['timestamp'], dist_id=device_info['dist_id'], video_url=device_info['video_url'])
            device_mysql.save()

    def get_device_info(self, request_id):
        if Drone.objects.filter(id=request_id).exists():
            device_mysql = Drone.objects.get(id=request_id)
            device_info = {
                'latitude': device_mysql.latitude,
                'longitude': device_mysql.longitude,
                'altitude': device_mysql.altitude,
                'dist_id': device_mysql.dist_id,
                'timestamp': device_mysql.timestamp,
                'video_url': device_mysql.video_url,
                'status': device_mysql.enabled
            }
            return device_info
        else:
            return None
        
    def delete_device(self, request_id):
        if Drone.objects.filter(id=request_id).exists():
            device_mysql = Drone.objects.get(id=request_id)
            device_mysql.delete()
            return True
        else:
            return False
    
    def updateImage(self, request_id, video_url):
        if Drone.objects.filter(id=request_id).exists():
            device_mysql = Drone.objects.get(id=request_id)
            device_mysql.video_url = video_url
            device_mysql.save()
            return True
        else:
            return False
    
    def disable_device(self, request_id):
        if Drone.objects.filter(id=request_id).exists():
            device_mysql = Drone.objects.get(id=request_id)
            device_mysql.enabled = False
            device_mysql.save()
            return True
        else:
            return False
    
    def get_all_devices(self):
        devices = Drone.objects.all().order_by('id')
        device_info = {"drones": {"0":[], "1":[], "2":[], "3":[], "4":[], "5":[], "6":[], "7":[], "8":[], "9":[], "10":[], "11":[], "12":[]}}
        for device in devices:
            data = {
                'id': device.id,
                'latitude': device.latitude,
                'longitude': device.longitude,
                'altitude': device.altitude,
                'dist_id': device.dist_id,
                'timestamp': device.timestamp,
                'video_url': device.video_url,
                'status': 'active' if device.enabled else 'inactive'
            }
            device_info["drones"][str(device.dist_id)].append(data)
            device_info["drones"]["0"].append(data)
            
        return device_info
    
    #add a new incident, if theres one already, update the timestamp instead
    def add_incidents(self,lat,lon,Type, district):
        #lat decimal with 5 decimal place
        lat = Decimal(lat).quantize(Decimal('1.00000'))
        #lon decimal with 5 decimal place
        lon = Decimal(lon).quantize(Decimal('1.00000'))

        if Incident.objects.filter(latitude=lat,longitude=lon, district=district).exists():
            incident = Incident.objects.get(latitude=lat,longitude=lon, district=district)
            incident.timestamp = timezone.now()
            incident.save()
            return False
        else:
            incident = Incident(latitude=lat,longitude=lon,type=Type, district=district)
            incident.save()
        return True
    
    def get_all_incidents(self):
        incidents = Incident.objects.all()
        incident_info = {"0":[], "1":[], "2":[], "3":[], "4":[], "5":[], "6":[], "7":[], "8":[], "9":[], "10":[], "11":[], "12":[]}
        for incident in incidents:
            data = {
                'id': incident.id,
                'latitude': incident.latitude,
                'longitude': incident.longitude,
                'timestamp': str(incident.timestamp),
                'description': incident.source,
                'dist_id': incident.district
            }
            incident_info[str(incident.district)].append(data)
            incident_info["0"].append(data)
        return incident_info
    