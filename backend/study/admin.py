from django.contrib import admin

from study.models import Dataset, Study, Classification


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['title', 'archive', 'file_count']
    exclude = ['file_count']
    readonly_fields = ['file_list']


@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ['title', 'pub_date', 'end_date', 'group', 'dataset', 'ui']


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    pass
