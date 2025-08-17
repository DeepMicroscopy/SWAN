import abc
import csv

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import JSONField
from django.http import HttpResponse
from django.template import engines
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
    list_display = ['study']
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
    list_display = ['title', 'pub_date', 'end_date', 'group', 'dataset', 'ui', 'share', 'educational']

    def share(self, study):
        context = {"study": study}
        template = """
            <a href="{% url 'share-users' study=study.id %}" target="_blank">Download</a>
        """

        return django_engine.from_string(template).render(context)

    @staticmethod
    def educational(study):
        return study.solution is not None

    share.short_description = "QR Code"
    share.allow_tags = False


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
        return [entry.user]


@admin.register(ClassificationAnonymous)
class ClassificationAnonymousAdmin(ClassificationAdmin):
    list_filter = ['study__title', 'session']
    list_display = ['date', 'study', 'session', 'index', 'choice']

    def csv_header(self):
        return ["session"]

    def csv_data(self, entry):
        return [entry.session]
