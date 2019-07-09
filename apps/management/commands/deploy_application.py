import subprocess
from django.core.management.base import BaseCommand
from apps.models import Application


class Command(BaseCommand):
    help = 'Perform the deploy of a specified application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--app',
            type=str,
            help='Application github name'
        )

    def handle(self, *args, **options):
        try:
            print('Running command')
            webhook = options.get('webhook')
            app = Application.objects.get(repository=options.get('app'))
            result = subprocess.run(['sh', app.deploy_script])
            return result
        except KeyError:
            print('Error deploying the app -- You have not specified the required --app parameter!')
            return result
