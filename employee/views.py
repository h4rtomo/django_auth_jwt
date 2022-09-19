from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from .serializers import UserSerializer
from .models import User

import jwt
from datetime import datetime, timedelta


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data['email']
        user = User.objects.filter(email=email).first()
        if user:
            raise ValidationError("Email already used")

        serializer.save()

        return Response({'success': 'Register Success'})


class LoginView(APIView):
    def post(self, request):

        try:
            email = request.data['email']
            password = request.data['password']
        except:
            return ValidationError('email / password is required')

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("Unauthenticated")

        if not user.check_password(password):
            raise AuthenticationFailed("Unauthenticated")

        now = datetime.now()
        expired = now + timedelta(minutes=10)

        payload = {
            'id': user.id,
            'exp': expired,
            'iat': now
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.data = {
            'token': token,
            'expired': expired
        }

        return response


class UserView(APIView):
    def get(self, request):
        try:
            token = request.headers['Authorization'].split("Bearer ")[1]
        except:
            raise AuthenticationFailed('Authorization is required!')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
