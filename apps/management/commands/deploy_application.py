import subprocess
from django.core.management.base import BaseCommand
from apps.models import Application, Deploy


class Command(BaseCommand):
    help = 'Perform the deploy of a specified application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--app',
            type=str,
            help='Application github name'
        )

    def handle(self, *args, **options):
        deploy = Deploy()
        app = Application.objects.get(repository=options.get('app'))
        deploy.app = app
        deploy.status = 'DNG'

        try:
            result = subprocess.run(['bash', app.deploy_script])
            deploy.status = 'DONE'
            return result
        except KeyError:
            deploy.status = 'KO'
            print('Error deploying the app -- You have not specified the required --app parameter!')
            return result
