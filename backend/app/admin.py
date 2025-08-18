import abc
import csv

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import JSONField
from django.http import HttpResponse
from django.template import engines
from django.urls import reverse
from django.utils.html import format_html
from django_json_widget.widgets import JSONEditorWidget

from app.models import User, Dataset, Study, ClassificationUser, ClassificationAnonymous, Solution, Ui

django_engine = engines['django']


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['title', 'archive', 'file_count']
    exclude = ['file_count']
    readonly_fields = ['file_list']


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ['study', 'archive']
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }


@admin.register(Ui)
class UiAdmin(admin.ModelAdmin):
    list_display = ['title']
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }


@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ['title', 'start', 'end', 'group', 'anonymous', 'educational', 'share', 'export']

    @staticmethod
    def start(study):
        return study.pub_date.strftime("%Y-%m-%d")

    @staticmethod
    def end(study):
        return study.end_date.strftime("%Y-%m-%d")

    @staticmethod
    def share(study):
        if study.anonymous:
            url = reverse("share-anonymous", args=[study.id])
        else:
            url = reverse("share-users", args=[study.id])

        return format_html(
            '<a href="{}" target="_blank">QR</a> / <a href="{}" target="_blank">URL<a/>',
            url, reverse("share-link", args=[study.id])
        )

    @staticmethod
    def export(study):
        url = reverse("export-csv", args=[study.id])
        return format_html('<a href="{}" target="_blank">CSV</a>', url)

    def educational(self, study) -> bool:
        return study.solution is not None

    educational.boolean = True


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
        raise NotImplemented

    @abc.abstractmethod
    def csv_data(self, entry):
        raise NotImplemented


@admin.register(ClassificationUser)
class ClassificationUserAdmin(ClassificationAdmin):
    list_filter = ['study__title', 'user']
    list_display = ['date', 'study', 'user', 'index', 'choice']

    def csv_header(self):
        return ["user"]

    def csv_data(self, entry):
        return [entry.user.id]


@admin.register(ClassificationAnonymous)
class ClassificationAnonymousAdmin(ClassificationAdmin):
    list_filter = ['study__title', 'session']
    list_display = ['date', 'study', 'session', 'index', 'choice']

    def csv_header(self):
        return ["session"]

    def csv_data(self, entry):
        return [entry.session]
