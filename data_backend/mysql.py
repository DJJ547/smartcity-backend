from .models import Camera, Iot, Drone, Incident, Congestion
from datetime import datetime, timedelta
import jwt

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

    # def update_new_incidents(self, current_time):
    #     entry_found = False
    #     with open(os.path.join(settings.STATIC_DIRS[0], 'all_text_chp_incident_day_2024_04_30.txt'), 'r') as file:
    #         for line in file:
    #             data = line.strip().split(',')
    #             parsed_datetime = datetime.strptime(data[3], "%m/%d/%Y %H:%M:%S")
    #             if current_time.hour == parsed_datetime.hour and current_time.minute == parsed_datetime.minute:
    #                 if Incident.objects.filter(id=data[0]).exists():
    #                     return False
    #                 else:
    #                     incident_mysql = Incident(id=data[0], timestamp=timezone.make_aware(current_time, timezone.get_current_timezone()), latitude=data[9], longitude=data[10],
    #                                               district=data[11], description=data[4], location=data[5], area=data[6])
    #                     incident_mysql.save()
    #                     entry_found = True
    #     if entry_found:
    #         return True
    #     else:
    #         return False

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