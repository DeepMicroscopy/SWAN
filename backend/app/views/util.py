from django.db.models import Q

from app import util
from app.models import Study


def study_queryset_for_request(request):
    if request.user.is_authenticated:
        return Study.objects.filter(Q(group__in=util.groups(request)) | Q(group__isnull=True))
    else:
        return Study.objects.filter(anonymous=True)
