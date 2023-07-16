from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.translation import gettext_lazy as _

@api_view()
@permission_classes([AllowAny])
def hi(request):
    return Response({"message": _("Hello world!")})
