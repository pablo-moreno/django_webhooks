from django.urls import path
from webhooks.views import GithubWebhookHandler, GitlabWebhookHandler


urlpatterns = [
    path('github', GithubWebhookHandler.as_view(), name='github-webhook-handler'),
    path('gitlab', GitlabWebhookHandler.as_view(), name='gitlab-webhook-handler'),
]
