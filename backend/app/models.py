import datetime
import uuid

from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from app import util
from swan.settings import AUTH_USER_MODEL


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    objects = models.Manager()

    class Meta:
        abstract = True

class DecoratorMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def upload_to(name):
    today = datetime.date.today()
    return f'{name}/{today.year}/{today.month}/{today.day}/{uuid.uuid4().hex}'


def upload_to_dataset(instance, filename):
    return upload_to("dataset")


def upload_to_solution(instance, filename):
    return upload_to("solution")


def upload_to_image(instance, filename):
    return upload_to("image")


class Dataset(UUIDModel, DecoratorMixin):
    title = models.CharField(max_length=200)
    archive = models.FileField(upload_to=upload_to_dataset)
    file_count = models.PositiveIntegerField(null=True, blank=True)
    file_list = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.archive:
            self.file_list = util.extract_file_names(self.archive.path)
            self.file_count = len(self.file_list)

            super().save(update_fields=['file_list', 'file_count'])


def ui_default():
    return {'left': {'text': 'left', 'icon': None, 'color': None}, 'right': {'text': 'right'}}


class Ui(UUIDModel, DecoratorMixin):
    title = models.CharField(max_length=200)
    labels = models.JSONField(default=ui_default)

    def __str__(self):
        return self.title


class Study(UUIDModel, DecoratorMixin):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to=upload_to_image, null=True, blank=True, help_text="(optional) A title image for the study.")
    description = models.TextField(null=True, blank=True, help_text="(optional) A short description of the study. Markdown is supported.")

    pub_date = models.DateTimeField("Start")
    end_date = models.DateTimeField("End")

    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, help_text="(optional) Limit access to members of this group.")
    anonymous = models.BooleanField(default=bool, help_text="Adds an authentication tag to the URL allowing anonymous access.")
    dataset = models.ForeignKey(Dataset, on_delete=models.PROTECT, help_text="This should not be changed later.")

    ui = models.ForeignKey(Ui, on_delete=models.PROTECT, help_text="This should not be changed later.")

    def __str__(self):
        return self.title


class Solution(DecoratorMixin):
    study = models.OneToOneField(Study, on_delete=models.CASCADE, primary_key=True)
    archive = models.FileField(upload_to=upload_to_solution)
    config = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return str(self.study)


class Classification(UUIDModel):
    date = models.DateTimeField()
    study = models.ForeignKey(Study, on_delete=models.PROTECT)
    file = models.CharField(max_length=200)
    choice = models.CharField(max_length=200)
    index = models.PositiveIntegerField()

    class Meta:
        abstract = True


class ClassificationUser(Classification):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Classification (User)"
        verbose_name_plural = "Classifications (User)"


class ClassificationAnonymous(Classification):
    session = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Classification (Anonymous)"
        verbose_name_plural = "Classifications (Anonymous)"
