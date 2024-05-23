from .models import User
from datetime import datetime, timedelta
import jwt

class MysqlProcessor:
    def __init__(self):
        pass
    
    def authenticate_user(self, email, password):
        if User.objects.filter(email=email, password=password).exists():
            user = User.objects.get(email=email, password=password)
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
            new_user = User(email=email, firstname=firstname, lastname=lastname, password=password)
            new_user.save()
            return {'result': True, 'message':'registration succeed'}