from django.db import models

class User(models.Model):
    email = models.CharField(max_length=100, unique=True, primary_key=True)
    password = models.CharField(max_length=100, null=False)
    firstname = models.CharField(max_length=100, null=False)
    lastname = models.CharField(max_length=100, null=False)
    is_agent = models.IntegerField(null=True)

    class Meta:
        db_table = 'users'
