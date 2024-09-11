from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny 
from .models import User,Code
from rest_framework import status
from django.utils.crypto import get_random_string
from .serializers import *
from .tasks import *
import datetime
# Create your views here.

@api_view(["POST"])
@permission_classes([AllowAny])
def registerView(request):
    if request.method == "POST":
        try:
            serial = UserSerializer(data=request.data)
            if serial.is_valid():
                if not User.objects.filter(username = request.data['username']).exists():
                    user=User(username = request.data["username"],email = request.data["email"])
                    if request.data.get("is_organizer"):
                        user.is_organizer=request.data["is_organizer"]
                    if request.data['password'] == request.data['confirm']:
                        user.password = make_password(request.data["password"])
                        user.save()
                        token=Token.objects.get_or_create(user=user)

                        return Response({"username":user.username,"token":str(token[0])}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"message":"password did't match"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    
                else:
                    return Response({"message":"username already exist"}, status=status.HTTP_403_FORBIDDEN)
            else :
                return Response(serial.errors, status=status.HTTP_403_FORBIDDEN)
        except Exception as error:
            return Response({"error":str(error)}, status=status.HTTP_403_FORBIDDEN)
        
@api_view(["POST"]) 
@permission_classes([AllowAny])
def resetview(request):
        try:
            email = request.data['email']
            code = get_random_string(length=5)
            while Code.objects.filter(code=code).exists():
                code = get_random_string(length=5)
            expired = datetime.datetime.now()+datetime.timedelta(minutes=1)
            reset = Code()
            user = User.objects.get(email=email)
            reset.profile = user
            reset.code = code
            reset.expire = expired
            reset.save()
            sending_mail.delay(request.data['email'],code)
            return Response("Sending email",status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({"error":str(error)},status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"]) 
@permission_classes([AllowAny])
def changeview(request,code):
    try:
        if Code.objects.get(code=code).expire.replace(tzinfo=None) >datetime.datetime.now():
            if request.data['password'] == request.data['confirm']:
                user = Code.objects.get(code=code).profile
                user.password=make_password(request.data['password'])
                user.save()
                Code.objects.get(code=code).delete()
                return Response({"message":"password changed"},status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"message":"password did't match"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            Code.objects.get(code=code).delete()
            return Response({"message":"token is expired"},status=status.HTTP_408_REQUEST_TIMEOUT)
    except Exception as error:
        return Response({"error":str(error)},status=status.HTTP_403_FORBIDDEN)
    

class CustomObtainAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny] 
