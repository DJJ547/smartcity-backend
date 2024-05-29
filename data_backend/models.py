from django.db import models
     
class Camera(models.Model):
    id = models.IntegerField(unique=True, null=False, primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    index = models.IntegerField(unique=True, null=False)
    time = models.DateTimeField()
    image_url = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    district = models.IntegerField()
    enabled = models.SmallIntegerField()
    video_url = models.CharField(max_length=500)

    class Meta:
        db_table = 'cameras'
        
class Iot(models.Model):
    station_id = models.IntegerField(primary_key=True, null=False)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    address = models.CharField(max_length=48)
    district = models.IntegerField(null=False)
    hourlySpeed = models.CharField(max_length=512)
    enabled = models.SmallIntegerField()

    class Meta:
        db_table = 'iots'
        
class Drone(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.IntegerField()
    status = models.CharField(max_length=45)
    dist_id = models.CharField(max_length=12)
    timestamp = models.DateTimeField()
    video_url = models.CharField(max_length=500)

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