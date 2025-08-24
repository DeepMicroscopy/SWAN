import abc
import csv

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import JSONField
from django.forms import model_to_dict
from django.http import HttpResponse
from django.template import engines
from django.urls import reverse
from django.utils.html import format_html
from django_json_widget.widgets import JSONEditorWidget

from app import util
from app.models import User, Dataset, Study, ClassificationUser, ClassificationAnonymous, Solution, Ui

django_engine = engines['django']

def fieldset(model, stuff):
    changed_fields = [t for s in stuff if s[1]["fields"] for t in s[1]["fields"]]
    forbidden_fields = ["id", "created_at", "updated_at"]

    fields = list(model_to_dict(model).keys())
    return (
        (None, {"fields": [f for f in fields if f not in changed_fields and f not in forbidden_fields]}),
    ) + stuff


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['title', 'archive', 'file_count', 'created_at', 'updated_at']
    readonly_fields = ['file_count', 'file_list']
    ordering = ['-updated_at']

    def get_fieldsets(self, request, obj=None):
        return fieldset(self.model,(
            ("General", {"fields": ["title", "archive"]}),
            ("Internal", {"fields": ["file_count", "file_list"], "classes": ["collapse"]}),
        ))


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ['study', 'created_at', 'updated_at', 'archive']
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }
    ordering = ['-updated_at']

    def get_fieldsets(self, request, obj=None):
        return fieldset(self.model,(
            ("General", {"fields": ["study", "archive", "config"]}),
            ("Interface", {"fields": ["label_current", "label_proof", "css_row", "css_column"], "classes": ["collapse"]}),
        ))


@admin.register(Ui)
class UiAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }
    ordering = ['-updated_at']

    def get_fieldsets(self, request, obj=None):
        return fieldset(self.model,(
            ("General", {"fields": ["title", "labels"]}),
        ))

    class Media:
        css = {
            "all": ("admin/css/white_space.css",)
        }


@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'group', 'pub_date', 'end_date',
        'anonymous', 'educational', 'share', 'export',
        'created_at', 'updated_at',
    ]
    ordering = ['-updated_at']

    def get_fieldsets(self, request, obj=None):
        return fieldset(self.model, (
            ("General", {"fields": ["title", "image", "description"]}),
            ("Configuration", {"fields": ["dataset", "ui"]}),
            ("Publication", {"fields": ["pub_date", "end_date"]}),
            ("Access", {"fields": ["group", "anonymous"]}),
        ))

    def educational(self, study) -> bool:
        return study.solution is not None

    educational.boolean = True

    @staticmethod
    def share(study):
        if study.anonymous:
            url = reverse("share-anonymous", args=[study.id])
            link = f"/#/studies/{study.id}/{util.create_tag(str(study.id))}"
        else:
            url = reverse("share-users", args=[study.id])
            link = f"/#/studies/{study.id}"

        return format_html(
            '<a href="{}" target="_blank">QR</a> / <a href="{}" target="_blank">URL<a/>',
            url, link
        )

    @staticmethod
    def export(study):
        url = reverse("export-csv", args=[study.id])
        return format_html('<a href="{}" target="_blank">CSV</a>', url)

    class Media:
        css = {
            "all": ("admin/css/wide_table.css",)
        }


class ClassificationAdmin(admin.ModelAdmin):
    actions = ["export_csv"]

    @admin.action(description="Export as CSV")
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type="text/plain")
        writer = csv.writer(response)
        writer.writerow(["time", "study", "file", "choice"] + self.csv_header())

        for entry in queryset:
            writer.writerow(
                [int(entry.date.timestamp()), entry.study.id, entry.file, entry.choice] + self.csv_data(entry)
            )

        return response

    @abc.abstractmethod
    def csv_header(self):
        raise NotImplementedError

    @abc.abstractmethod
    def csv_data(self, entry):
        raise NotImplementedError


@admin.register(ClassificationUser)
class ClassificationUserAdmin(ClassificationAdmin):
    list_filter = ['study__title', 'user']
    list_display = ['date', 'study', 'user', 'index', 'choice']
    ordering = ['-date']

    def csv_header(self):
        return ["user"]

    def csv_data(self, entry):
        return [entry.user.id]


@admin.register(ClassificationAnonymous)
class ClassificationAnonymousAdmin(ClassificationAdmin):
    list_filter = ['study__title', 'session']
    list_display = ['date', 'study', 'session', 'index', 'choice']
    ordering = ['-date']

    def csv_header(self):
        return ["session"]

    def csv_data(self, entry):
        return [entry.session]
