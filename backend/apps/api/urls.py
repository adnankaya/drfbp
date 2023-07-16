from rest_framework import routers
from django.urls import path, include

# internals
from . import views

from .jwt import CustomTokenObtainPairView

app_name = "api"

urlpatterns = [
    path('hi/', views.hi, name='hi'),
    path('tokens/', CustomTokenObtainPairView.as_view(), name='token-obtain'),
    path('users/', include("apps.users.urls", namespace="users")),
]
