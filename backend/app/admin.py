from django.contrib import admin

from app.models import Dataset, Study, ClassificationUser, ClassificationAnonymous


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['title', 'archive', 'file_count']
    exclude = ['file_count']
    readonly_fields = ['file_list']


@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ['title', 'pub_date', 'end_date', 'group', 'dataset', 'ui']


@admin.register(ClassificationUser)
class ClassificationAdmin(admin.ModelAdmin):
    list_display = ['date', 'study', 'user', 'index', 'choice']

@admin.register(ClassificationAnonymous)
class ClassificationAdmin(admin.ModelAdmin):
    list_display = ['date', 'study', 'session', 'index', 'choice']
