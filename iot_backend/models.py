from django.db import models

class Station_Speed(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    station_id = models.IntegerField(null=False)
    speed = models.FloatField(null=False)
    flow = models.FloatField(null=False)
    timestamp = models.DateTimeField(null=False)

    class Meta:
        db_table = 'iot_speed_flow_every_5min'
        unique_together = (('station_id', 'timestamp'),)
        