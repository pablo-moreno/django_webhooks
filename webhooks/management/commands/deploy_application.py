import subprocess
from django.core.management.base import BaseCommand
from webhooks.models import Application, Deploy
import logging

logger = logging.getLogger('deploy_command')


class Command(BaseCommand):
    help = 'Perform the deploy of a specified application'

    def add_arguments(self, parser):
        parser.add_argument('--app', type=str, help='Application github name')
        parser.add_argument('--app_version', type=str, help='New version to be deployed')

    def handle(self, *args, **options):
        app, version = options.get('app'), options.get('app_version')

        logger.info(f'Running deploy for {app}@{version}')
        deploy = Deploy()
        app = Application.objects.get(repository=app)
        deploy.app = app
        deploy.status = Deploy.DNG

        # Run deploy script
        try:

            command = ['bash', app.deploy_script]
            result = subprocess.run(command)

            if result.returncode == 0:
                logger.info('Deploy finished succesfully')
                deploy.status = Deploy.OK
                app.version = version
                app.save()
            else:
                logger.error('Deploy finished with errors')
                deploy.status = Deploy.KO

        except Exception as e:
            logger.error(f'Error deploying application: {e}')
            deploy.status = Deploy.KO

        finally:
            deploy.save()
