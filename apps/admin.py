from django.contrib import admin
from apps.models import Application, WebHook, Deploy

admin.site.register(Application)
admin.site.register(Deploy)
admin.site.register(WebHook)
