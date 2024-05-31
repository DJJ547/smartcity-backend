from pymongo import MongoClient
from django.utils import timezone
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os
import pytz
load_dotenv()
mongodbpassword = quote_plus(os.getenv('mongodbpassword'))
mongodb_uri = f"mongodb://{os.getenv('mongodbusername')}:{mongodbpassword}@{os.getenv('mongodbhost')}:27017/"


class MongoDBProcessor:
    def __init__(self):
        # mongoDB connection
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[os.getenv('mongodb_name')]
        self.drone_collection = self.db['drones']

    # get device info
    def get_drone_info(self, id):
        drone_info = self.drone_collection.find_one({'id': id})
        if drone_info is None:
            return None
        id = drone_info['id']
        dist_id = drone_info['dist_id']
        latitude = drone_info['latitude']
        longitude = drone_info['longitude']
        altitude = drone_info['altitude']
        video_url = drone_info['video_url']
        print(video_url)
        timestamp = timezone.now()
        return {'id': id, 'dist_id': dist_id, 'latitude': latitude, 'longitude': longitude, 'altitude': altitude, 'time': timestamp, 'video_url': video_url}

    # search by index or address
    def search_device(self, search_term):
        result = []
        try:
            search_term_int = int(search_term)
            numeric_search = {"$eq": search_term_int}
        except ValueError:
            numeric_search = None

        search_conditions = [{"id": numeric_search}, {"dist_id": numeric_search}]

        drones = self.drone_collection.find({"$or": search_conditions}).limit(100)
        for drone in drones:
            data = {
                'latitude': drone['latitude'],
                'longitude': drone['longitude'],
                'id': drone['id'],
                'dist_id': drone['dist_id'],
                'address': '',
            }
            result.append(data)
        return result


if __name__ == '__main__':
    mongodb = MongoDBProcessor()
    print(mongodb.get_drone_info(1))
    print(mongodb.search_device('1'))
