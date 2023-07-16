from rest_framework import routers
from django.urls import path, include

# internals
from . import views


app_name = "users"

user_detail = views.UserViewset.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',


})

urlpatterns = [

    path('', views.ListUsersAPIView.as_view(), name='list-users'),
    path('signup/', views.CreateUserAPIView.as_view(), name='create-user'),
    path('<int:pk>/', user_detail, name='detail-user'),
    path('<int:pk>/deactivate/', views.DeactivateUserView.as_view(), name='deactivate-user'),
    path('<int:pk>/password-change/',
         views.UserViewset.as_view(
             {'put': 'password_change', 'patch': 'password_change'}),
         name='password-change'),

]
