import datetime

import magic
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, FileResponse

from app.models import Study


def index_studies(request):
    now = datetime.datetime.now(datetime.UTC)
    groups = request.user.groups.values_list("id", flat=True)

    return JsonResponse(list(Study.objects.filter(pub_date__lte=now, end_date__gt=now, group__in=groups).values_list('id', flat=True)), safe=False)

def study(request, uuid):
    groups = request.user.groups.values_list("id", flat=True)

    result = Study.objects.filter(id=uuid, group__in=groups).values().first()
    if result is None:
        raise PermissionDenied

    return JsonResponse(result)

def study_image(request, uuid):
    groups = request.user.groups.values_list("id", flat=True)

    result = Study.objects.filter(id=uuid, group__in=groups).first()
    if result is None:
        raise PermissionDenied

    path = result.image.path
    return FileResponse(open(path, 'rb'), content_type=magic.from_file(path, mime=True))