from django.db import models


class Application(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=240, blank=True, null=True)
    repository = models.URLField(unique=True)
    deploy_script = models.FilePathField()
    version = models.CharField(max_length=10, blank=True, null=True)


class WebHook(models.Model):
    type = models.CharField(max_length=50)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True)
    action = models.CharField(max_length=24, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    author = models.CharField(max_length=16, blank=True, null=True)
    version = models.CharField(max_length=16, blank=True, null=True)
    prerelease = models.BooleanField(default=True)

    @staticmethod
    def from_request(request):
        webhook_type = request.META.get('HTTP_X_GITHUB_EVENT', None)
        webhook_data = request.data
        webhook = WebHook()
        webhook.type = webhook_type

        if webhook_type == 'release':
            webhook.action = webhook_data.get('action')
            webhook.url = webhook_data.get('release', {}).get('url')
            webhook.author = webhook_data.get('release', {}).get('author', {}).get('login')
            webhook.version = webhook_data.get('release', {}).get('tag_name', None)
            webhook.prerelease = webhook_data.get('release', {}).get('prerelease', True)

        return webhook


class Deploy(models.Model):
    DEPLOY_STATUSES = (
        ('PEN', 'PENDING'),
        ('DNG', 'DOING'),
        ('OK', 'DONE'),
        ('KO', 'ERROR'),
    )

    app = models.ForeignKey(Application, on_delete=models.CASCADE, null=True)
    webhook = models.ForeignKey(WebHook, on_delete=models.CASCADE, null=True)
    started_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=DEPLOY_STATUSES, max_length=16)
