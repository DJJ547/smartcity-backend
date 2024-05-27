from django.contrib.auth.models import User
from datetime import datetime, timedelta
import pytz
import jwt

class MysqlProcessor:
    def __init__(self):
        pass
    
    def authenticate_user(self, email, password):
        if User.objects.filter(email=email, password=password).exists():
            user = User.objects.get(email=email, password=password)
            user.is_active = 1
            user.last_login = pytz.utc.localize(datetime.now())
            user.save()
            # generate JWT token
            payload = {
                'email': user.email,
                'exp': datetime.now() + timedelta(minutes=60)
            }
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            return {'result': True, 'message': 'login succeed', 'user': user, 'token':token}
        else:
            return {'result': False, 'message': 'login failed, invalid credential'}
        
    def register_user(self, email, password, firstname, lastname):
        user = User.objects.filter(email=email)
        if user.exists():
            return {'result': False, 'message':'registration failed, email already exist'}
        else:
            new_user = User(email=email, first_name=firstname, last_name=lastname, password=password, is_superuser=0, username='/', is_staff=0, is_active=0, date_joined=pytz.utc.localize(datetime.now()))
            new_user.save()
            return {'result': True, 'message':'registration succeed'}