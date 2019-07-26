import hmac
from django.db import models
from string import digits, ascii_letters
from random import choice


class Secret(models.Model):
    app = models.CharField(max_length=32)
    secret = models.CharField(max_length=32, blank=True, null=True, db_index=True)

    def verify_signature(self, request):
        signature = request.headers.get('X-Hub-Signature', None)

        if not signature:
            raise Exception('Signature not found')

        sha_name, sign = signature.split('=')
        mac = hmac.new(self.secret, msg=request.data, digestmod='sha1')

        return hmac.compare_digest(mac.hexdigest(), sign)

    def save(self, *args, **kwargs):
        if not self.secret:
            self.secret = ''.join([choice(digits + ascii_letters) for _ in range(0, 32)])
        super().save(*args, **kwargs)


class Application(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=240, blank=True, null=True)
    repository = models.URLField(unique=True)
    deploy_script = models.CharField(max_length=200, blank=True, null=True)
    version = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f'{self.name}@{self.version}'


class WebHook(models.Model):
    type = models.CharField(max_length=50)
    repository = models.URLField(blank=True, null=True)
    action = models.CharField(max_length=24, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    author = models.CharField(max_length=16, blank=True, null=True)
    version = models.CharField(max_length=16, blank=True, null=True)
    prerelease = models.BooleanField(default=True)

    @staticmethod
    def from_request(request):
        secret = Secret.objects.get(app='Github')
        verified = secret.verify_signature(request)

        if not verified:
            raise Exception('Invalid signature')

        webhook = WebHook()
        webhook_type = request.META.get('HTTP_X_GITHUB_EVENT', None)
        data = request.data
        webhook.type = webhook_type
        webhook.repository = data.get('repository', {}).get('html_url')
        webhook.action = data.get('action')

        if webhook_type == 'release':
            webhook.url = data.get('release', {}).get('url')
            webhook.author = data.get('release', {}).get('author', {}).get('login')
            webhook.version = data.get('release', {}).get('tag_name', None)
            webhook.prerelease = data.get('release', {}).get('prerelease', True)

        return webhook


class Deploy(models.Model):
    PEN = 'PEN'
    DNG = 'DNG'
    OK = 'OK'
    KO = 'KO'

    DEPLOY_STATUSES = (
        (PEN, 'PENDING'),
        (DNG, 'DOING'),
        (OK, 'DONE'),
        (KO, 'ERROR'),
    )

    app = models.ForeignKey(Application, on_delete=models.CASCADE, null=True)
    started_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=DEPLOY_STATUSES, max_length=16)
