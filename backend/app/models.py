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


def upload_to(name):
    today = datetime.date.today()
    return f'{name}/{today.year}/{today.month}/{today.day}/{uuid.uuid4().hex}'


def upload_to_dataset(instance, filename):
    return upload_to("dataset")


def upload_to_solution(instance, filename):
    return upload_to("solution")


def upload_to_image(instance, filename):
    return upload_to("image")


class Dataset(UUIDModel):
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


class Ui(UUIDModel):
    title = models.CharField(max_length=200)
    labels = models.JSONField(default=ui_default)

    def __str__(self):
        return self.title


class Study(UUIDModel):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to=upload_to_image, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    pub_date = models.DateTimeField()
    end_date = models.DateTimeField()

    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    anonymous = models.BooleanField(default=bool)
    dataset = models.ForeignKey(Dataset, on_delete=models.PROTECT)

    ui = models.ForeignKey(Ui, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class Solution(models.Model):
    study = models.OneToOneField(Study, on_delete=models.CASCADE, primary_key=True)
    archive = models.FileField(upload_to=upload_to_solution)
    config = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return str(self.study)


class Classification(UUIDModel):
    date = models.DateTimeField("entry time")
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
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
