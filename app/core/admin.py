from django.contrib import admin  # noqa
from core import models


admin.site.register(models.User)
admin.site.register(models.Contract)
admin.site.register(models.Garden)
