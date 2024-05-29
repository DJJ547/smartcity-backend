from pymongo import MongoClient
from django.utils import timezone
from dotenv import load_dotenv
import os
load_dotenv()

class MongoDBProcessor:
    def __init__(self):
        #mongoDB connection
        self.client = MongoClient(os.getenv('mongodb_uri'))
        self.db = self.client['smartcity']
        self.camera_collection = self.db['Camera']

    # get device info   
    def get_camera_info(self, id):
        camera_info = self.camera_collection.find_one({'ID': id})
        if camera_info is None:
            return None
        id = camera_info['ID']
        index = camera_info['index']
        district = camera_info['district']
        address = (camera_info['nearbyPlace'] if 'nearbyPlace' in camera_info else '') + ', ' + (camera_info['locationName'] if 'locationName' in camera_info else '')
        latitude = camera_info['latitude']
        longitude = camera_info['longitude']
        image_url = camera_info['currentImageURL']
        video_url = camera_info['streamingVideoURL'] if 'streamingVideoURL' in camera_info else ''
        time = str(timezone.now())
        return {'id': id, 'index': index, 'district': district, 'address': address, 'latitude': latitude, 'longitude': longitude, 'image_url': image_url, 'time': time, 'video_url': video_url}
    
    # search by index or address
    def search_device(self, search_term):
        result = []
        regex = {"$regex": f".*{search_term}.*"}

        for camera in self.camera_collection.find({"$or": [{"index": regex}, {"nearbyPlace": regex}, {"locationName": regex}, {"district": regex}]}).limit(100):
            data = {
                'latitude': camera['latitude'],
                'longitude': camera['longitude'],
                'id': camera['ID'],
                'index': camera['index'],
                'image_url': camera['currentImageURL'],
                'address': (camera['nearbyPlace'] if 'nearbyPlace' in camera else '') + ', ' + (camera['locationName'] if 'locationName' in camera else ''),
                'dist_id': camera['district'],
                'time': str(timezone.now()),
                'video_url': camera['streamingVideoURL'] if 'streamingVideoURL' in camera else ''
            }
            result.append(data)
        return result
    

    