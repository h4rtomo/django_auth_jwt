import datetime

import jwt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from employee.serializers import UserSerializer
from config import settings
from .models import User


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data['email']
        user = User.objects.filter(email=email).first()
        if user:
            raise ValidationError('email already used')

        serializer.save()
        response = Response()
        response.data = {'success': 'Register Success'}

        return response


class LoginView(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']
        except:
            raise ValidationError('email / password is required')

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('Unauthenticated !')

        if not user.check_password(password):
            raise AuthenticationFailed('Unauthenticated !')

        now = datetime.datetime.now()
        expired = now + datetime.timedelta(minutes=10)
        payload = {
            'id': user.id,
            'exp': expired,
            'iat': now
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        response = Response()

        response.data = {
            'token': token,
            'expired': expired
        }

        return response


class ProfileView(APIView):
    def get(self, request):
        # data = auth_middleware(request)
        # return Response(data)
        try:
            token = request.headers['Authorization'].split("Bearer ")[1]

            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['id']
            user = User.objects.filter(id=user_id).first()
            serializer = UserSerializer(user)

            return Response(serializer.data)
        except:
            raise AuthenticationFailed('Unauthenticated !')


def auth_middleware(request):
    try:
        token = request.headers['Authorization'].split("Bearer ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['id']
        user = User.objects.filter(id=user_id).first()
        serializer = UserSerializer(user)

        return serializer.data
    except:
        raise AuthenticationFailed('Unauthenticated!')
