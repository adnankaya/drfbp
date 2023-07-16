from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework import status, generics, views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import PermissionDenied
from django.utils.translation import gettext as _
# internals
from apps.core.mixins import MultiSerializerViewSetMixin
from apps.core.permissions import IsAdminOrIsSelf
from .serilaizers import (UserSerializer, UserUpdateSerializer,
                          UserCreateSerializer, PasswordChangeSerializer)

User = get_user_model()


class UserViewset(MultiSerializerViewSetMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    serializer_action_classes = {
        "update": UserUpdateSerializer,
        "password_change": PasswordChangeSerializer,
    }

    @action(detail=True, methods=["put", "patch"],
            url_name="password-change", permission_classes=[IsAdminOrIsSelf])
    def password_change(self, request, pk=None):
        user = self.get_object()
        # Check permissions before serializer validation
        if not IsAdminOrIsSelf().has_permission(request, self):
            raise PermissionDenied(_(
                "You do not have permission to change this password"))

        serializer = PasswordChangeSerializer(data=request.data,
                                              context={"request": request})
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'message': 'password changed'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class CreateUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ListUsersAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DeactivateUserView(views.APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
