from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.
class User(AbstractUser):
    is_organizer = models.BooleanField(null=False,default=False)

class Code(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.OneToOneField(User,blank=False,on_delete=models.CASCADE)
    code = models.CharField(max_length=100,blank=False)
    expire = models.DateTimeField(null=False,blank=False)