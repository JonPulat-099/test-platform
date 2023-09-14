from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'
from django.core.management import BaseCommand

from main.models import BaseUser, UserGroup


class Command(BaseCommand):
    help = 'Cron testing'

    def handle(self, *args, **options):

        data = [
            {"lang": 2, "name": "MIN-10", "users": [{"name": "ERMATOVA ShOHISTAXON ABDULAZIZ QIZI"}]}
        ]
        for i in data:
            group = UserGroup.objects.create(name=i['name'], language=i['lang'])
            for user in i['users']:
                last_id = BaseUser.objects.last()
                BaseUser.objects.create(
                    first_name=user['name'], is_student=True, username=str(last_id.id)+user['name'][0],
                    password='123'
                )
        self.stdout.write(self.style.SUCCESS('Successfully withdrown money from apartment accounts'))
