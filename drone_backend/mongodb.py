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
        #mongoDB connection
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[os.getenv('mongodb_name')]
        self.camera_collection = self.db['drone']

    # get device info   
    def get_drone_info(self, id):
        drone_info = self.drone_collection.find_one({'id' : id})
        print(id, drone_info)
        if drone_info is not None:
            latitude = drone_info['latitude']
            longitude = drone_info['longitude']
            altitude = drone_info['altitude']
            dist_id = drone_info['dist_id']
            timestamp = str(timezone.now())
            video_url = drone_info['video_url']
            status = drone_info['status']
        
        return {'drone_id': id, 'latitude': latitude, 'longitude': longitude, 'altitude': altitude,  'timestamp':timestamp ,'dist_id': dist_id, 'video_url': video_url, 'status': status}
    
    
    