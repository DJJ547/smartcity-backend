from django.db import models

class Station_Speed(models.Model):
    station_id = models.IntegerField(null=False)
    speed = models.IntegerField(null=False)
    timestamp = models.DateTimeField(null=False)

    class Meta:
        db_table = 'iot_speed_every_5min'
        unique_together = (('station_id', 'timestamp'),)
        