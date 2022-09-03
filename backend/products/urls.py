from django.contrib import admin
from django.urls import path
from .views import ProductViewSet,RegistrationView,LoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('products', ProductViewSet.as_view({
        'get': 'list',
        'post': 'create',

    })),

    path('products/<str:pk>', ProductViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',

    })),

    path('user/registration',RegistrationView.as_view()),
    path( 'user/login', LoginView.as_view()),
    path( 'token/', TokenObtainPairView.as_view(), name='token_obtain_pair' ),
    path( 'token/refresh/', TokenRefreshView.as_view(), name='token_refresh' ),

]
