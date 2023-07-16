# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate Users'

    

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            "\nProcess started...{}\n").format(__name__))

        try:
            with transaction.atomic():
                User.objects.create_user(email='member@example.com',
                                        username='member',
                                        phone='5555555555',
                                        password='qwert')
                User.objects.create_superuser(email='admince@example.com',
                                                   username='admince',
                                                   phone='5555555556',
                                                   password='qwert')
        except Exception as e:
            raise e

        self.stdout.write(self.style.SUCCESS("Process finished"))
