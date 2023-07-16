from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['id'] = user.id
        token['first_name'] = user.first_name
        token['full_name'] = user.get_full_name()
        token['email'] = user.email
        token['last_name'] = user.last_name
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser

        return token

    def validate(self, attrs):
        """
        Customized to get token by username or email or phone
        """
        credentials = {
            'username': attrs.get('username'),
            'password': attrs.get("password")
        }
        try:
            query = attrs.get('username')
            user = User.objects.get(Q(username=query) |
                                    Q(email=query) |
                                    Q(phone=query))
            if user:
                credentials['username'] = user.username
        except:
            pass
        return super().validate(credentials)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
