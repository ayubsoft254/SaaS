from django.db import models

# Create your models here.
class PageVisits(models.Model):
    path = models.TimeField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)   
