from rest_framework.permissions import BasePermission
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _
from rest_framework.request import Request
from django.views.generic.base import View


class AllowAnonymousUser(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsAdminOrIsSelf(BasePermission):
    # def has_object_permission(self, request, view, obj):
    #     breakpoint()
    #     return super().has_object_permission(request, view, obj)

    def has_permission(self, request: Request, view: View):
        if request.user.is_staff:
            return True

        is_self_user = view.get_object() == request.user
        if not is_self_user:
            raise ValidationError(
                _("Requested user is not the owner of this user object"))
        return is_self_user
