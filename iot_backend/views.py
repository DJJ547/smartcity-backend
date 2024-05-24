from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .mysql import MysqlProcessor

@api_view(['GET'])
def get_all_data(request):
    mysql = MysqlProcessor()
    devices = mysql.get_all_devices()
    return Response({'devices': devices}, status=status.HTTP_200_OK)


