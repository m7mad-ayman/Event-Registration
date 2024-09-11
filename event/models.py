from django.db import models
from account.models import *
import uuid

# Create your models here.
class Event(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    organizer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='organizer')

    title = models.CharField(max_length=500,null=False,blank=False)
    description = models.CharField(max_length=1000,null=False,blank=False)
    date = models.DateTimeField(null=False)
    location = models.CharField(max_length=500,null=False,blank=False)
    capacity = models.IntegerField(null=False)
    available= models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    

class Registration(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='register')
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='registed')
    registration_date = models.DateTimeField(auto_now=True,null=False)
    def __str__(self):
        return '{} , {}'.format(self.user.username,self.event.title)
