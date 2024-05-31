from pymongo import MongoClient
from django.utils import timezone
from dotenv import load_dotenv
from statistics import mean
from datetime import datetime, timedelta
from .models import Station_Speed
from data_backend.models import Iot, Congestion
from urllib.parse import quote_plus
import os
import pytz
from django.conf import settings
load_dotenv()
mongodbpassword = quote_plus(os.getenv('mongodbpassword'))
mongodb_uri = f"mongodb://{os.getenv('mongodbusername')}:{mongodbpassword}@{os.getenv('mongodbhost')}:27017/"

class MongoDBProcessor:
    def __init__(self):
        # mongoDB connection
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[str(os.getenv('mongodb_name'))]
        self.iot_collection = self.db['iots_all']

    # get device info
    def get_iot_info(self, station_id):
        iot = self.iot_collection.find_one({'id': station_id})
        if iot is None:
            return None
        return {
            'id': iot['id'],
            'freeway': iot['freeway'],
            'direction': iot['direction'],
            'city': iot['city'],
            'county': iot['county'],
            'latitude': iot['latitude'],
            'longitude': iot['longitude'],
            'district': iot['district'],
        }

    # Search by station_id or freeway or district
    def search_iot_info(self, search_term):
        result = []
        try:
            search_term_int = int(search_term)
            numeric_search = {"$eq": search_term_int}
        except ValueError:
            numeric_search = None

        search_conditions = [{"id": numeric_search}, {"district": numeric_search}, {"freeway": numeric_search}]

        iot_info = self.iot_collection.find({"$or": search_conditions}).limit(100)
 
        for iot in iot_info:
            station_id = iot['id']
            address = str(iot['freeway']) + ' ' + str(iot['direction'])
            latitude = iot['latitude']
            longitude = iot['longitude']
            district = iot['district']
            result.append({
                'id': station_id,
                'address': address,
                'dist_id': district,
                'latitude': latitude,
                'longitude': longitude
            })
        return result

    def update_all_flow_speed_congestion_in_5min(self, time):
        if not isinstance(time, datetime):
            time = pytz.utc.localize(
                datetime.strptime(time, "%Y-%m-%d %H:%M:%S"))
        now = datetime.now()
        total_minutes = time.hour * 60 + time.minute
        index = total_minutes // 5
        all_id = Iot.objects.values_list('station_id', flat=True)
        all_id_list = list(all_id)
        all_station_data = self.iot_collection.find({})
        for station in all_station_data:
            if station['id'] in all_id_list:
                data_time = pytz.utc.localize(datetime.strptime(
                    station['speed_flow_every_5min'][index]['timestamp'], "%m/%d/%Y %H:%M:%S").replace(year=now.year, month=now.month, day=now.day))
                if Station_Speed.objects.filter(timestamp=data_time, station_id=station['id']).exists():
                    return
                new_station_speed = Station_Speed(station_id=station['id'], speed=station['speed_flow_every_5min']
                                                  [index]['speed'], flow=station['speed_flow_every_5min'][index]['flow'], timestamp=data_time)
                new_station_speed.save()
                # formula to calculate density = flow/speed, threshhold for urban highway is 35~45
                if station['speed_flow_every_5min'][index]['flow'] * 12 // station['speed_flow_every_5min'][index]['speed'] > 45:
                    new_congestion = Congestion(
                        timestamp=data_time, source='iot', source_id=station['id'], latitude=station['latitude'], longitude=station['longitude'], district=station['district'])
                    new_congestion.save()
        return

    def update_all_flow_speed_congestions_from_0am_to_now(self, time):
        if not isinstance(time, datetime):
            time = pytz.utc.localize(
                datetime.strptime(time, "%Y-%m-%d %H:%M:%S"))
        now = datetime.now()
        total_minutes = time.hour * 60 + time.minute
        index = total_minutes // 5
        all_id = Iot.objects.values_list('station_id', flat=True)
        all_id_list = list(all_id)
        all_station_data = self.iot_collection.find({})
        for station in all_station_data:
            if station['id'] in all_id_list:
                for i in range(0, index + 1):
                    parsed_time = pytz.utc.localize(datetime.strptime(
                        station['speed_flow_every_5min'][i]['timestamp'], "%m/%d/%Y %H:%M:%S").replace(year=now.year, month=now.month, day=now.day))
                    print(parsed_time)
                    if Station_Speed.objects.filter(timestamp=parsed_time, station_id=station['id']).exists():
                        print("skipped speed")
                        continue
                    new_station_speed = Station_Speed(
                        station_id=station['id'], speed=station['speed_flow_every_5min'][i]['speed'], flow=station['speed_flow_every_5min'][i]['flow'], timestamp=parsed_time)
                    new_station_speed.save()
                    # formula to calculate density = flow/speed, threshhold for urban highway is 35~45
                    if station['speed_flow_every_5min'][i]['flow'] * 12 // station['speed_flow_every_5min'][i]['speed'] > 40:
                        print(station['speed_flow_every_5min'][i]['flow'] *
                              12 // station['speed_flow_every_5min'][i]['speed'])
                        if Congestion.objects.filter(timestamp=pytz.utc.localize(datetime.strptime(station['speed_flow_every_5min'][i]['timestamp'], "%m/%d/%Y %H:%M:%S")), source='iot', source_id=station['id']).exists():
                            print("skipped conges")
                            continue
                        new_congestion = Congestion(
                            timestamp=parsed_time, source='iot', source_id=station['id'], latitude=station['latitude'], longitude=station['longitude'], district=station['district'])
                        new_congestion.save()
        return

    def test_add_iots_given_list(self, iot_id_list):
        for iot_id in iot_id_list:
            if Iot.objects.filter(station_id=iot_id).exists():
                continue
            iot_info = self.iot_collection.find_one({'id': iot_id})
            iot = Iot(station_id=iot_info['id'], freeway=iot_info['freeway'] if str(iot_info['freeway']) else '', direction=iot_info['direction'] if iot_info['direction'] else '', city=iot_info['city']
                      if iot_info['city'] else '', county=iot_info['county'] if iot_info['county'] else '', latitude=iot_info['latitude'], longitude=iot_info['longitude'], district=iot_info['district'], enabled=1)
            iot.save()
        return
