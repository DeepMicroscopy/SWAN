import datetime
import uuid

from django.contrib.auth.models import Group, User, AbstractUser
from django.db import models

from app.util import extract_file_names
from swan.settings import AUTH_USER_MODEL


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


def upload_to(name):
    today = datetime.date.today()
    return f'{name}/{today.year}/{today.month}/{today.day}/{uuid.uuid4().hex}'


def upload_to_dataset(instance, filename):
    return upload_to("dataset")


def upload_to_image(instance, filename):
    return upload_to("image")


class Dataset(UUIDModel):
    objects = models.Manager()

    title = models.CharField(max_length=200)
    archive = models.FileField(upload_to=upload_to_dataset)
    file_count = models.PositiveIntegerField(null=True, blank=True)
    file_list = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.archive:
            self.file_list = extract_file_names(self.archive.path)
            self.file_count = len(self.file_list)

            super().save(update_fields=['file_list', 'file_count'])


class UiType(models.IntegerChoices):
    DEFAULT = 1, 'Default'


class Study(UUIDModel):
    objects = models.Manager()

    title = models.CharField(max_length=200)
    image = models.FileField(upload_to=upload_to_image)

    pub_date = models.DateTimeField("publication date")
    end_date = models.DateTimeField("date the study ends")

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)

    ui = models.IntegerField(
        choices=UiType.choices,
        default=UiType.DEFAULT
    )

    def __str__(self):
        return self.title


class Classification(UUIDModel):
    objects = models.Manager()

    date = models.DateTimeField("entry time")
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    file = models.CharField(max_length=200)
    choice = models.PositiveSmallIntegerField()
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