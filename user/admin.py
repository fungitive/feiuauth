from django.contrib import admin
from django.apps import apps
# Register your models here.
from . import models

all_models = apps.get_app_config('user').get_models()
for model in all_models:
    try:
        admin.site.register(model)
    except:
        pass
