from django.urls import path
from .views import *

urlpatterns = [
    path('events/', eventsView,name="events"),
    path('events/<str:id>/register/',registrationView,name='registration'),
    path('events/<str:id>',eventView,name='event')
]