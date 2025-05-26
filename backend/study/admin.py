from django.contrib import admin

from study.models import Dataset, Study, Classification

admin.site.register(Dataset)
admin.site.register(Study)
admin.site.register(Classification)