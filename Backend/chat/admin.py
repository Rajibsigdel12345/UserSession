from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Connection)
admin.site.register(models.Groups)
admin.site.register(models.Messages)
