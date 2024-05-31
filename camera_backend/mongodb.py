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
        try:
            search_term_int = int(search_term)
            numeric_search = {"$eq": search_term_int}
        except ValueError:
            numeric_search = None

        search_conditions = [{"ID": numeric_search}, {"district": numeric_search}]
        if numeric_search is not None:
            search_conditions.extend([{"nearbyPlace": regex}, {"locationName": regex}])

        for camera in self.camera_collection.find({"$or": search_conditions}).limit(100):
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
    

    