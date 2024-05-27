from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .mysql import MysqlProcessor
    
@api_view(['GET'])
def get_all_data(request):
    mysql = MysqlProcessor()
    devices = mysql.get_all_devices()
    # incidents = mysql.get_all_incidents()
    return Response({'devices': devices}, status=status.HTTP_200_OK)


# @api_view(['POST'])
# def update_incidents(request):
#     json_data = json.loads(request.body)
#     time = json_data.get('currentTime')
#     request_time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
#     mysql = MysqlProcessor()
#     result = mysql.update_new_incidents(request_time)
#     return Response(result, status=status.HTTP_200_OK)

# @api_view(['POST'])
# def update_congestions(request):
#     json_data = json.loads(request.body)
#     time = json_data.get('currentTime')
#     mongodb = MongoDBProcessor()
#     iot_speeds = mongodb.get_congestions_given_time(time)
#     # mysql = MysqlProcessor()
#     # mysql.update_congestions(iot_speeds)
#     return Response(iot_speeds, status=status.HTTP_200_OK)