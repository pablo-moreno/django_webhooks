from django.urls import path
from apps.views import WebhookHandler


urlpatterns = [
    path('', WebhookHandler.as_view(), name='deploy-app'),
]