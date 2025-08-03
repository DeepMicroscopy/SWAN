import datetime
import json
import os.path
import random

import magic
from django import forms
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render

from app.models import Study, Classification, ClassificationUser, ClassificationAnonymous
from app.util import extract_file_data, deterministic_shuffle, seed_from
from swan.settings import MEDIA_ROOT


def groups(request):
    return request.user.groups.values_list("id", flat=True)

class Question1Form(forms.Form):
    study = forms.CharField()
    choice = forms.IntegerField()
    index = forms.IntegerField()

# noinspection DuplicatedCode
def classify(request):
    if request.method == "GET":
        return render(request, 'classify.html', {'form': Question1Form()})

    data = {}

    if request.content_type == "application/x-www-form-urlencoded":
        form = Question1Form(request.POST)
        if not form.is_valid():
            return JsonResponse(form.errors.as_json(), status=400)
        data = form.cleaned_data

    result = Study.objects.filter(id=data["study"], group__in=groups(request)).select_related("dataset").first()
    if result is None:
        raise PermissionDenied

    if data["index"] >= result.dataset.file_count:
        return HttpResponse(status=400)

    items = deterministic_shuffle(result.dataset.file_list, seed_from(request.user, request.session, data["study"]))

    data["file"] = items[data["index"]]

    if request.user.username == "anonymous":
        result, created = ClassificationAnonymous.objects.create(date=datetime.datetime.now(), session=request.session.session_key, study_id=data["study"], file=data["file"], choice=data["choice"], index=data["index"])
        return JsonResponse(ClassificationAnonymous.objects.filter(id=result.id).values().first(), safe=False)
    else:
        result = ClassificationUser.objects.create(date=datetime.datetime.now(), user=request.user, study_id=data["study"], file=data["file"], choice=data["choice"], index=data["index"])
        return JsonResponse(ClassificationUser.objects.filter(id=result.id).values().first(), safe=False)

def index_studies(request):
    now = datetime.datetime.now(datetime.UTC)
    return JsonResponse(list(Study.objects.filter(pub_date__lte=now, end_date__gt=now, group__in=groups(request)).values_list('id', flat=True)), safe=False)

def study(request, uuid):
    result = Study.objects.filter(id=uuid, group__in=groups(request)).values().first()
    if result is None:
        raise PermissionDenied

    return JsonResponse(result)

def study_image(request, uuid):
    result = Study.objects.filter(id=uuid, group__in=groups(request)).first()
    if result is None:
        raise PermissionDenied

    path = result.image.path
    return FileResponse(open(path, 'rb'), content_type=magic.from_file(path, mime=True))


def study_index(request, uuid):
    if request.user.username == "anonymous":
        result = ClassificationUser.objects.filter(study=uuid, session=request.session.session_key, study__group__in=groups(request)).order_by("-index").first()
    else:
        result = ClassificationUser.objects.filter(study=uuid, user=request.user, study__group__in=groups(request)).order_by("-index").first()

    if result is None:
        return JsonResponse(0, safe=False)

    return JsonResponse(result.index, safe=False)

def study_entry(request, uuid, index):
    result = Study.objects.filter(id=uuid, group__in=groups(request)).select_related("dataset").first()
    if result is None:
        raise PermissionDenied

    if index >= result.dataset.file_count:
        return HttpResponse(status=204)

    items = deterministic_shuffle(result.dataset.file_list, seed_from(request.user, request.session, uuid))
    file_data = extract_file_data(os.path.join(MEDIA_ROOT, result.dataset.archive.path), items[index])

    return HttpResponse(file_data, content_type=magic.from_buffer(file_data, mime=True))

@permission_required("view_dataset")
def index_datasets(request):
    raise NotImplemented


@permission_required("view_dataset")
def dataset(request):
    raise NotImplemented

@permission_required("view_dataset")
def dataset_image(request):
    raise NotImplemented