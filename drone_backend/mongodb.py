from pymongo import MongoClient
from django.utils import timezone
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os
load_dotenv()
mongodbpassword = quote_plus(os.getenv('mongodbpassword'))
mongodb_uri = f"mongodb://{os.getenv('mongodbusername')}:{mongodbpassword}@{os.getenv('mongodbhost')}:27017/"

class MongoDBProcessor:
    def __init__(self):
        #mongoDB connection
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[os.getenv('mongodb_name')]
        self.drone_collection = self.db['drones']

    # get device info   
    def get_drone_info(self, id):
        drone_info = self.drone_collection.find_one({'id': id})
        if drone_info is None:
            return None
        id = drone_info['id']
        district = drone_info['dist_id']
        latitude = drone_info['latitude']
        longitude = drone_info['longitude']
        video_url = drone_info['video_url']
        time = str(timezone.now())
        return {'id': id,'district': district, 'latitude': latitude, 'longitude': longitude, 'time': time, 'video_url': video_url}
    
    # search by index or address
    def search_device(self, search_term):
        result = []
        regex = {"$regex": f".*{search_term}.*"}
        try:
            search_term_int = int(search_term)
            numeric_search = {"$eq": search_term_int}
        except ValueError:
            numeric_search = None

        search_conditions = [{"id": numeric_search}, {"dist_id": numeric_search}]

        for drone in self.drone_collection.find({"$or": search_conditions}).limit(100):
            data = {
                'latitude': drone['latitude'],
                'longitude': drone['longitude'],
                'id': drone['id'],
                'dist_id': drone['dist_id'],
                'time': str(timezone.now()),
                'video_url': drone['video_url']
            }
            result.append(data)
        print(result)
        return result
    
if __name__ == '__main__':
    mongodb = MongoDBProcessor()
    print(mongodb.get_drone_info(1))
    print(mongodb.search_device('1'))
    