import datetime
import uuid

from django.contrib.auth.models import Group, User
from django.db import models

from models.base import UUIDModel

def upload_to_dataset(instance, filename):
    today = datetime.date.today()
    return f'datasets/{today.year}/{today.month}/{today.day}/{uuid.uuid4().hex}'

class Dataset(UUIDModel):
    title = models.CharField(max_length=200)
    archive = models.FileField(upload_to=upload_to_dataset)

class UiType(models.IntegerChoices):
    DEFAULT = 1, 'Default'

class Study(UUIDModel):
    title = models.CharField(max_length=200)

    pub_date = models.DateTimeField("publication date")
    end_date = models.DateTimeField("date the study ends")

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)

    ui = models.IntegerField(
        choices=UiType.choices,
        default=UiType.DEFAULT
    )

class Classification(UUIDModel):
    date = models.DateTimeField("entry time")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    file = models.CharField(max_length=200)
    choice = models.IntegerField()