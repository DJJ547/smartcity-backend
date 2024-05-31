from django.db import models
     
class Camera(models.Model):
    id = models.IntegerField(unique=True, null=False, primary_key=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    index = models.IntegerField(unique=True, null=False)
    time = models.DateTimeField()
    image_url = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    district = models.IntegerField()
    enabled = models.BooleanField(default=True)
    video_url = models.CharField(max_length=500)

    class Meta:
        db_table = 'cameras'
        
class Iot(models.Model):
    station_id = models.IntegerField(primary_key=True, null=False)
    freeway = models.CharField(max_length=45)
    direction = models.CharField(max_length=45)
    city = models.CharField(max_length=45)
    county = models.CharField(max_length=45)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    district = models.IntegerField(null=False)
    enabled = models.BooleanField(default=True)

    class Meta:
        db_table = 'iots'
        
class Drone(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    altitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    dist_id = models.IntegerField(null=False)
    timestamp = models.DateTimeField()
    video_url = models.CharField(max_length=500)
    enabled = models.BooleanField(default=True)

    class Meta:
        db_table = 'drones'

class Incident(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    timestamp = models.DateTimeField(null=False)
    source = models.CharField(max_length=45, null=False)
    source_id = models.IntegerField(null=False)
    description = models.CharField(max_length=500)
    location = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    district = models.IntegerField(null=False)
    
    class Meta:
        db_table = 'incidents'
        unique_together = (('source_id', 'timestamp'),)
        

class Congestion(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    timestamp = models.DateTimeField(null=False)
    source = models.CharField(max_length=45, null=False)
    source_id = models.IntegerField(null=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    district = models.IntegerField(null=False)
    
    class Meta:
        db_table = 'congestions'
        unique_together = (('source_id', 'timestamp'),)