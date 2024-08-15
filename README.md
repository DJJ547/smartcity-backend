# smartcity-backend
This "Smart City Traffic AI Cloud Platform" project aims to improve traffic management in smart cities by developing a cloud-based system that utilizes artificial intelligence (AI) and big data collected from CCTV cameras, IoT devices, and drone images. This platform will provide functionalities for both city traffic agents and the public clients.

## Frontend Project Layout
```
smartcity-backend/
├── auth_system/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── mysql.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
├── camera_backend/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── mongodb.py
│   ├── mysql.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
├── data_backend/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── mysql.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
├── drone_backend/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── mongodb.py
│   ├── mysql.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
├── iot_backend/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── mongodb.py
│   ├── mysql.py
│   ├── tasks.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
├── smartcity_backend/
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── detection.py
│   ├── iotAI.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── static/
├── gitignore
├── manage.py
├── README.md
├── requirements.txt
```

## How to run our React back-end locally:
- install python. https://www.python.org/downloads/
- run the following command to install the libraries from requirements.txt.
```
pip install -r requirements.txt
```
- start Redis from command prompt.
- set up MySQL and MongoDB databases (backup databases are in our shared Google drive) in an AWS EC2 instance, update configurations in settings.py accordingly.
- To run celery in order to update incidents, flow & speed periodically, run this two commands in a new terminal
```
celery -A smartcity_backend worker -l info --pool=solo
``` 
```
celery -A smartcity_backend beat -l info
``` 
- run this command to run locally
```
python manage.py runserver
``` 
