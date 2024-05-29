from pymongo import MongoClient
from django.utils import timezone
from dotenv import load_dotenv
from statistics import mean
from datetime import datetime, timedelta
from .models import Station_Speed
from data_backend.models import Iot, Incident, Congestion
import os
import pytz
from django.conf import settings
load_dotenv()

class MongoDBProcessor:
    def __init__(self):
        #mongoDB connection
        self.client = MongoClient(os.getenv('mongodb_uri'))
        self.db = self.client[str(os.getenv('mongodb_name'))]
        self.iot_collection = self.db['iots_all']
        
    # get device info
    def get_iot_info(self, station_id):
        iot_info = self.iot_collection.find_one({'station_id': int(station_id)})

        # return iot_info
        station_id = iot_info['station_id']
        address = str(iot_info['Fwy']) + ' ' + str(iot_info['Dir'])
        latitude = iot_info['location'][0]
        longitude = iot_info['location'][1]
        district = iot_info['District']
        hourlySpeed = self.get_hourly_speed(station_id)

        return {
            'station_id': station_id,
            'address': address,
            'district': district,
            'latitude': latitude,
            'longitude': longitude,
            'hourlySpeed': hourlySpeed
        }

    # Search by station_id or freeway or district
    def search_iot_info(self, search):
        if search.strip() == '':
            return []
        try:
            search_int = int(search)
        except ValueError:
            search_int = None

        query = {'$or': []}
        if search_int is not None:
            query['$or'].extend([{'station_id': search_int}, {'Fwy': search_int}])
        query['$or'].append({'District': search})

        iot_info = self.iot_collection.find(query).limit(100)
        iot_data = []
        for iot in iot_info:
            station_id = iot['station_id']
            address = str(iot['Fwy']) + ' ' + str(iot['Dir'])
            latitude = iot['location'][0]
            longitude = iot['location'][1]
            district = iot['District']
            iot_data.append({
                'id': station_id,
                'address': address,
                'district': district,
                'latitude': latitude,
                'longitude': longitude
            })
        return iot_data
    
    def get_hourly_speed(self, station_id):
        # Fetch data from MongoDB
        station_data = self.iot_collection.find_one({"station_id": station_id})

        # Process timeseries data
        timeseries = station_data['timeseries']
        hourly_speeds = []

        # Group data by hour and calculate average speed
        for i in range(24):
            hour_data = [entry['Speed'] for entry in timeseries[i*12:(i+1)*12]]
            if hour_data and not any(x is None for x in hour_data):  # Ensure there is data to average
                average_speed = mean(hour_data)
                # Round the average speed to two decimal places
                rounded_average = round(average_speed, 2)
                hourly_speeds.append(rounded_average)
            else:
                # Append a default value or handle missing data as needed
                hourly_speeds.append(0.00)  # Example default value

        return hourly_speeds
    
    def update_all_flow_speed_congestion_in_5min(self, time):
        if not isinstance(time, datetime):
            time = pytz.utc.localize(datetime.strptime(time, "%Y-%m-%d %H:%M:%S"))
        total_minutes = time.hour * 60 + time.minute
        index = total_minutes // 5     
        all_id = Iot.objects.values_list('station_id', flat=True)
        all_id_list = list(all_id)
        all_station_data = self.iot_collection.find({})
        for station in all_station_data:
            if station['id'] in all_id_list:
                data_time = pytz.utc.localize(datetime.strptime(station['speed_flow_every_5min'][index]['timestamp'], "%m/%d/%Y %H:%M:%S").replace(month=pytz.utc.localize(datetime.now()).month, day=pytz.utc.localize(datetime.now()).day))
                if Station_Speed.objects.filter(timestamp=data_time, station_id=station['id']).exists():
                    return
                new_station_speed = Station_Speed(station_id=station['id'], speed=station['speed_flow_every_5min'][index]['speed'], flow=station['speed_flow_every_5min'][index]['flow'], timestamp=data_time)
                new_station_speed.save()
                # formula to calculate density = flow/speed, threshhold for urban highway is 35~45
                if station['speed_flow_every_5min'][index]['flow'] * 12 // station['speed_flow_every_5min'][index]['speed'] > 45:
                    new_congestion = Congestion(timestamp=data_time, source='iot', source_id=station['id'], latitude=station['latitude'], longitude=station['longitude'], district=station['district'])
                    new_congestion.save()
        return
    
    def update_all_flow_speed_congestions_from_0am_to_now(self, time):
        if not isinstance(time, datetime):
            time = pytz.utc.localize(datetime.strptime(time, "%Y-%m-%d %H:%M:%S"))
        total_minutes = time.hour * 60 + time.minute
        index = total_minutes // 5
        all_id = Iot.objects.values_list('station_id', flat=True)
        all_id_list = list(all_id)
        all_station_data = self.iot_collection.find({})
        for station in all_station_data:
            if station['id'] in all_id_list:
                for i in range(0, index + 1):
                    parsed_time = pytz.utc.localize(datetime.strptime(station['speed_flow_every_5min'][i]['timestamp'], "%m/%d/%Y %H:%M:%S"))
                    print(parsed_time)
                    if Station_Speed.objects.filter(timestamp=parsed_time, station_id=station['id']).exists():
                        print("skipped speed")
                        continue
                    new_station_speed = Station_Speed(station_id=station['id'], speed=station['speed_flow_every_5min'][i]['speed'], flow=station['speed_flow_every_5min'][i]['flow'], timestamp=parsed_time)
                    new_station_speed.save()
                    # formula to calculate density = flow/speed, threshhold for urban highway is 35~45
                    if station['speed_flow_every_5min'][i]['flow'] * 12 // station['speed_flow_every_5min'][i]['speed'] > 40:
                        print(station['speed_flow_every_5min'][i]['flow'] * 12 // station['speed_flow_every_5min'][i]['speed'])
                        if Congestion.objects.filter(timestamp=pytz.utc.localize(datetime.strptime(station['speed_flow_every_5min'][i]['timestamp'], "%m/%d/%Y %H:%M:%S")), source='iot', source_id=station['id']).exists():
                            print("skipped conges")
                            continue
                        new_congestion = Congestion(timestamp=parsed_time, source='iot', source_id=station['id'], latitude=station['latitude'], longitude=station['longitude'], district=station['district'])
                        new_congestion.save()
        return