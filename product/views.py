from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer

from employee.views import auth_middleware


class CreateProductView(APIView):
    def post(self, request):
        _ = auth_middleware(request)

        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        response = Response()
        response.data = {'success': 'Create Product Success'}

        return response
