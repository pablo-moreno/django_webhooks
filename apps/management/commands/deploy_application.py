import subprocess
from django.core.management.base import BaseCommand
from apps.models import Application, Deploy


class Command(BaseCommand):
    help = 'Perform the deploy of a specified application'

    def add_arguments(self, parser):
        parser.add_argument('--app', type=str, help='Application github name')
        parser.add_argument('--app_version', type=str, help='New version to be deployed')

    def handle(self, *args, **options):
        deploy = Deploy()
        app = Application.objects.get(repository=options.get('app'))
        deploy.app = app
        deploy.status = 'DNG'

        # Run deploy script
        command = ['bash', app.deploy_script]
        result = subprocess.run(command)

        if result.returncode == 0:
            deploy.status = 'DONE'
            app.version = options.get('app_version', None)
            app.save()
        else:
            deploy.status = 'KO'

        deploy.save()
