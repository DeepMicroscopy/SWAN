import datetime

import magic
from django.http import JsonResponse, FileResponse

from study.models import Study


def index(request):
    now = datetime.datetime.now(datetime.UTC)

    return JsonResponse([x[0] for x in Study.objects.filter(pub_date__lte=now, end_date__gt=now, group__in=request.user.groups.values_list("id", flat=True)).values_list('id')], safe=False)

def image(request, id):
    path = Study.objects.get(id=id).image.path
    return FileResponse(open(path, 'rb'), content_type=magic.from_file(path, mime=True))