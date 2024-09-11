from django.urls import path
from .views import *

urlpatterns = [
    path('register/', registerView,name="register"),
    path('reset/',resetview,name='reset'),
    path('change/<str:code>',changeview,name='pasch'),

]