from pymongo import MongoClient
from django.utils import timezone
from dotenv import load_dotenv
from statistics import mean
from datetime import datetime, timedelta
from .models import Station_Speed
from data_backend.models import Iot
import os
import pytz
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
    
    def update_all_speed_in_5min(self, time):
        time = pytz.utc.localize(datetime.strptime(time, "%Y-%m-%d %H:%M:%S"))
        total_minutes = time.hour * 60 + time.minute
        index = total_minutes // 5     
        all_id = Iot.objects.values_list('station_id', flat=True)
        all_id_list = list(all_id)
        all_station_data = self.iot_collection.find({})
        for station in all_station_data:
            if station['id'] in all_id_list:
                data_time = pytz.utc.localize(datetime.strptime(station['speed_flow_every_5min'][index]['timestamp'], "%m/%d/%Y %H:%M:%S").replace(month=pytz.utc.localize(datetime.now()).month, day=pytz.utc.localize(datetime.now()).day))
                new_row = Station_Speed(station_id=station['id'], speed=station['speed_flow_every_5min'][index]['speed'], flow=station['speed_flow_every_5min'][index]['flow'], timestamp=data_time)
                new_row.save()
        return 'speed updated'
    