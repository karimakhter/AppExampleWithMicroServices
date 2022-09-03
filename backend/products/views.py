import logging

from django.contrib.auth import authenticate, login
from rest_framework import viewsets, status
from rest_framework.response import Response
from .producer import publish
from rest_framework.views import APIView
from .models import Product
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer,RegistrationSerializer
from .utils import get_tokens_for_user



class ProductViewSet( viewsets.ViewSet ):

    permission_classes = [IsAuthenticated, ]
    def list( self, request ):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        data =serializer.data
        publish(data,b'All Products')
        return Response(data)

    def create( self, request ):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish(serializer.data,b'Product Created')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve( self, request, pk=None ):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        data=serializer.data
        publish(data, b'Prodect reterived')
        return Response(data)

    def update( self, request, pk=None ):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish(serializer.data, b'Product Updated')
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy( self, request, pk=None ):
        try:
            product = Product.objects.get( id=pk )
            serializer = ProductSerializer(instance=product, data=request.data)
            serializer.is_valid(raise_exception=True)
            product.delete()
            publish(serializer.data, b'Product Deleted')
            logging.info("Product deleted")
            return Response( status=status.HTTP_204_NO_CONTENT )
        except:
            logging.error("Product does not exist")
            return  Response( status=status.HTTP_412_PRECONDITION_FAILED)


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        if 'username' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        username = request.data['username']
        password = request.data['password']
        logging.error(f"{username}")
        logging.error(f"{password}")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success', **auth_data}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

