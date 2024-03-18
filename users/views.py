from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import datetime
import jwt   #from pyjwt

# Create your views here.

class RegisterAPIView(APIView):

    def post(self, request): 

        serializer = UserSerializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)  #if anything not valid, raise exception
        serializer.save()
        return Response(serializer.data)
    

class LoginAPIView(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        #find user using email
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found:)')

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid password")
        
        payload = {
            "id": user.id,
            "email": user.email,
            "exp": datetime.datetime.now()+ datetime.timedelta(minutes=60),   #exp: expiration time
            "iat": datetime.datetime.now(),  #iat: issued at
        }


        token = jwt.encode(payload, 'secret', algorithm='HS256')

        # token.decode('utf-8')

        #setting token via cookies
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        #httponly -  frontend can't access cookie, only for backend

        response.data = {
            'message': "You are logged in!",
            'jwt token': token
        }

        #if password correct
        return response
    

#get user using cookies
class UserView(APIView):
    
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        #decode gets the user
        
        user = User.objects.filter(id=payload['id']).first()

        serializer = UserSerializer(user)
        
        print(serializer.data)

        return Response(serializer.data)
        #cookies accessed if preserved
    

class LogOutView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'You are logged out successfully.'
        }

        return response