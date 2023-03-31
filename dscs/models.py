from django.db import models

# Create your models here.
class Algorithm(models.Model):
    title =models.CharField(max_length=20)
    audience = models.IntegerField()
    release_date = models.DateField()
    genre = models.CharField(max_length=30)
    score = models.FloatField()
    poster_url = models.CharField(max_length=50)
    descripthion = models.TextField()