import abc
import csv

from django.contrib import admin
from django.http import HttpResponse
from django.template import engines

from app.models import User, Dataset, Study, ClassificationUser, ClassificationAnonymous
from django.contrib.auth.admin import UserAdmin

django_engine = engines['django']


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['title', 'archive', 'file_count']
    exclude = ['file_count']
    readonly_fields = ['file_list']


@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ['title', 'pub_date', 'end_date', 'group', 'dataset', 'ui', 'share']

    def share(self, study):
        context = {"study": study}
        template = """
            <a href="{% url 'study-share' uuid=study.id %}" target="_blank">Download</a>
        """

        return django_engine.from_string(template).render(context)

    share.short_description = "QR Code"
    share.allow_tags = False

class ClassificationAdmin(admin.ModelAdmin):
    actions = ["export_csv"]

    @admin.action(description="Export as CSV")
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type="application/json")
        writer = csv.writer(response)
        writer.writerow(["time", "study", "file", "choice"] + self.csv_header())

        for entry in queryset:
            writer.writerow([int(entry.date.timestamp()), entry.study.id, entry.file, entry.choice] + self.csv_data(entry))

        return response

    @abc.abstractmethod
    def csv_header(self):
        pass

    @abc.abstractmethod
    def csv_data(self, entry):
        pass


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
