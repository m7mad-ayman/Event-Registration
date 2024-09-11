from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
# Create your views here.
@api_view(["GET","POST"])
def eventsView(request):
    if request.method == "GET":
        events = Event.objects.all()
        serial = EventSerializer(events,many=True)
        return Response(serial.data,status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        if request.user.is_organizer :
            event = Event(organizer=request.user,title=request.data["title"],description=request.data["description"],date=request.data["date"],
                          location=request.data["location"],capacity=request.data["capacity"],available=request.data["capacity"])
        
            event.save()
            serial = EventSerializer(event)
            return Response(serial.data,status=status.HTTP_201_CREATED)
        else :
            return Response({"message":"you aren't an organizer"},status=status.HTTP_200_OK)

@api_view(["GET","PUT","DELETE"])
def eventView(request,id):
    event = Event.objects.get(id=id)
    if request.method == "GET":
        
        serial = EventSerializer(event)
        return Response(serial.data,status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        if request.user == event.organizer:
            serial = EventSerializer(event,data=request.data)
            if serial.is_valid():
                serial.save()
                return Response(serial.data,status=status.HTTP_201_CREATED)
            else:
                return Response({"message":"data isn't valid"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"you aren't the organizer of this event"},status=status.HTTP_200_OK)
        
    elif request.method == "DELETE":
        if request.user == event.organizer:
            event.delete()
            return Response({"message":"event deleted"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"you aren't the organizer of this event"},status=status.HTTP_200_OK)


@api_view(["GET","POST","DELETE"])
def registrationView(request,id):
    if request.method == "POST":
        event = Event.objects.get(id=id)
        user = request.user
        if event.available:
            if not Registration.objects.filter(event=event,user=user).exists():
                registration = Registration(event=event,user=user)
                registration.save()
                event.available -=1
                event.save()
                serial = RegistrationSerializer(registration)
                return Response(serial.data,status=status.HTTP_201_CREATED)
                

            else:
                return Response({"message":"you already registered"})
        else:
            return Response({"message":"sorry there are no empty places"})
        
    elif request.method == "GET":
        event = Event.objects.get(id=id)
        user = request.user
        if Registration.objects.filter(event=event,user=user).exists():
            registration = Registration.objects.get(event=event,user=user)
            serial = RegistrationSerializer(registration)
            return Response(serial.data,status=status.HTTP_200_OK)
        else:
            return Response({"message":"you don't have registration"})
    elif request.method == "DELETE":
        event = Event.objects.get(id=id)
        user = request.user
        if Registration.objects.filter(event=event,user=user).exists():
            registration = Registration.objects.get(event=event,user=user)
            registration.delete()
            event.available +=1
            event.save()
            return Response({"message":"your registration deleted"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"you don't have registration"})

