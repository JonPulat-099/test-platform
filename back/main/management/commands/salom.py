from django.core.management import BaseCommand
from main.utils import import_data


class Command(BaseCommand):
    help = 'Cron testing'

    def handle(self, *args, **options):
        import_data()
        self.stdout.write(self.style.SUCCESS('Successfully'))
