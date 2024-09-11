from rest_framework.serializers import ModelSerializer ,CharField
from .models import *

class EventSerializer(ModelSerializer):
    organizer = CharField(source='organizer.username', read_only=True)
    class Meta:
        model = Event
        fields = ["id","title","organizer","description","date","location","capacity","available","created_at"]
    
class RegistrationSerializer(ModelSerializer):
    class Meta:
        model = Registration
        fields = "__all__"