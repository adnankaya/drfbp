from django.db import models
from django.utils.translation import gettext_lazy as _


class Base(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        abstract = True
        default_manager_name = 'objects'


class Image(Base):
    class Status(models.TextChoices):
        ACTIVE = 'A', _('Active')
        PASSIVE = 'P', _('Passive')

    height = models.PositiveIntegerField(null=True, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=1, choices=Status.choices,
                              default=Status.ACTIVE)
    label = models.CharField(max_length=120, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ('order',)
