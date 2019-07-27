from django.urls import path
from webhooks.views import WebhookHandler


urlpatterns = [
    path('', WebhookHandler.as_view(), name='deploy-app'),
]