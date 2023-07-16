from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# internals

#  constants
User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=4096)
    profile_image = models.ImageField(upload_to='profile_images')

    class Meta:
        db_table = "t_profile"

    @property
    def profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url

    @property
    def profile_image_storage_backend(self):
        return settings.DEFAULT_FILE_STORAGE


class ProfileSettings(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    enabled = models.BooleanField(default=False)

    class Meta:
        db_table = "t_profile_settings"
