import uuid

from django.db.models import Q

from app import util
from app.models import Study


def study_queryset_for_request(request):
    if request.user.is_authenticated:
        return Study.objects.filter(Q(group__in=util.groups(request)) | Q(group__isnull=True))
    else:
        return Study.objects.filter(anonymous=True)


def session_for_request(request) -> str:
    if (
            not request.session.session_key
            or "anonymous" not in request.session
            or not request.session["anonymous"]
    ):
        request.session.create()
        request.session["anonymous"] = uuid.uuid4().hex

    return request.session["anonymous"]
