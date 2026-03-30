import datetime
import uuid

from django.contrib.auth.models import AbstractUser, Group
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.deconstruct import deconstructible

from app import util
from swan.settings import AUTH_USER_MODEL

allowed_extensions_archive = ['.zip', '.tar', '.tar.zst', '.tar.gz']
allowed_extensions_image = ['.png', '.jpg', '.jpeg']

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    intro_general = models.PositiveSmallIntegerField(default=0)
    intro_swiping = models.PositiveSmallIntegerField(default=0)


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


@deconstructible
class UploadTo(object):
    def __init__(self, name: str = "default", extensions: list[str] = None):
        self.name = name
        self.extensions = extensions

    def __call__(self, instance, filename):
        extension = next((x for x in self.extensions if filename.endswith(x)), None)
        if not extension:
            raise ValidationError("Invalid file extension.") # validator should have prevented this

        today = datetime.date.today()
        return f'{self.name}/{today.year}/{today.month}/{today.day}/{uuid.uuid4().hex}{extension}'


@deconstructible
class ValidatorExtension(object):
    def __init__(self, extensions: list[str] = None):
        self.extensions = extensions

    def __call__(self, value):
        for extension in self.extensions:
            if value.name.endswith(extension):
                return
        raise ValidationError("Extension not allowed. Allowed extensions: "+", ".join(self.extensions))


class Dataset(UUIDModel, DecoratorMixin):
    title = models.CharField(max_length=200, help_text="Only used for display purposes in the study creation.")
    archive = models.FileField(upload_to=UploadTo("dataset", allowed_extensions_archive), validators=[ValidatorExtension(allowed_extensions_archive)], help_text="The dataset archive. Files are registered by their full path inside the archive.")
    file_count = models.PositiveIntegerField(null=True, blank=True, help_text="The number of files in the dataset. Calculated automatically.")
    file_list = models.JSONField(null=True, blank=True, help_text="A list of all files in the dataset. Calculated automatically.")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.archive:
            self.file_list = util.extract_file_names(self.archive.path)
            self.file_count = len(self.file_list)

            super().save(update_fields=['file_list', 'file_count'])


class Directions(models.TextChoices):
    LEFT = "left", "left"
    RIGHT = "right", "right"
    UP = "up", "up"
    DOWN = "down", "down"

def ui_default():
    return {'left': {'text': 'left', 'icon': None, 'color': None}, 'right': {'text': 'right', 'label': 'bad'}}


class Ui(UUIDModel, DecoratorMixin):
    title = models.CharField(max_length=200, help_text="Only used for display purposes in the study creation.")
    labels = models.JSONField(default=ui_default, help_text="""A dictionary mapping the directions 'up', 'down', 'left' and 'right' to an object.
The object has the keys 'text', 'icon' and 'color' - 'label' can be used to rename the label in the export.""")
    postpone = models.CharField(max_length=200, choices=Directions, help_text="(optional) The direction to mark images for another round of classification.", null=True, blank=True)
    pixelated = models.BooleanField(default=True, help_text="Use 'pixelated' image-rendering.")
    default_scale = models.PositiveSmallIntegerField(default=100, help_text="The default scale of images in the study. Values in percent.")

    def __str__(self):
        return self.title


class Study(UUIDModel, DecoratorMixin):
    title = models.CharField(max_length=200, help_text="The title of the study. Visible in all interfaces.")
    image = models.ImageField(upload_to=UploadTo("image", allowed_extensions_image), validators=[ValidatorExtension(allowed_extensions_image)], null=True, blank=True, help_text="(optional) A title image for the study.")
    description = models.TextField(null=True, blank=True, help_text="(optional) A short description of the study. Markdown is supported.")

    pub_date = models.DateTimeField("Start", help_text="The study will be visible on the overview at this time.")
    end_date = models.DateTimeField("End", help_text="The study will be removed from the overview at this time.")

    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, help_text="(optional) Limit access to members of this group.")
    anonymous = models.BooleanField(default=bool, help_text="Adds an authentication tag to the URL allowing anonymous access.")
    dataset = models.ForeignKey(Dataset, on_delete=models.PROTECT, help_text="This should not be changed later.")

    ui = models.ForeignKey(Ui, on_delete=models.PROTECT, help_text="This should not be changed later.")

    def __str__(self):
        return self.title


class Solution(DecoratorMixin):
    study = models.OneToOneField(Study, on_delete=models.CASCADE, primary_key=True, help_text="The study that this solution belongs to.")
    archive = models.FileField(upload_to=UploadTo("solution", allowed_extensions_archive), validators=[ValidatorExtension(allowed_extensions_archive)], help_text="The solution archive. Solution images must have the same names as the dataset images.")
    config = models.JSONField(default=dict, blank=True, help_text="A dictionary mapping file names in the dataset to an object. The object has 'text' to be displayed and 'choice' for skipping matches. Markdown is supported.")

    label_current = models.CharField(max_length=200, null=True, blank=True, help_text="(optional) The label displayed for the classified image. Defaults to 'Current' in the frontend.")
    label_proof = models.CharField(max_length=200, null=True, blank=True, help_text="(optional) The label displayed for the proof. Defaults to 'Proof' in the frontend.")
    css_row = models.CharField(max_length=200, null=True, blank=True, help_text="(optional) The CSS class for the row. Overrides the frontend defaults.")
    css_column = models.CharField(max_length=200, null=True, blank=True, help_text="(optional) The CSS class for the column. Additional modifiers that are added to the frontend defaults.")

    def __str__(self):
        return str(self.study)


class Classification(UUIDModel):
    date = models.DateTimeField(help_text="The time the image was classified.")
    study = models.ForeignKey(Study, on_delete=models.PROTECT, help_text="The study that this classification belongs to.")
    file = models.CharField(max_length=200, help_text="The name of the file that was classified at the index of this dataset.")
    choice = models.CharField(max_length=5, choices=Directions, help_text="The direction the user swiped for the classification.")
    index = models.PositiveIntegerField(help_text="The index of the image based on the shuffled dataset for the user of this study.")

    class Meta:
        abstract = True


class ClassificationUser(Classification):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, help_text="The user who classified the image.")

    class Meta:
        verbose_name = "Classification (User)"
        verbose_name_plural = "Classifications (User)"

        indexes = [
            models.Index(fields=["user", "study", "index", "-date"]),
        ]


class ClassificationAnonymous(Classification):
    session = models.CharField(max_length=32, help_text="A unique identifier for the user's session, but not the session-id.")

    class Meta:
        verbose_name = "Classification (Anonymous)"
        verbose_name_plural = "Classifications (Anonymous)"

        indexes = [
            models.Index(fields=["session", "study", "index", "-date"]),
        ]
