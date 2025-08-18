from rest_framework import routers

from app.views.auth import AuthViewSet
from app.views.classify import ClassifyViewSet
from app.views.dataset import DatasetViewSet
from app.views.export import ExportViewSet
from app.views.share import ShareViewSet
from app.views.study import StudyViewSet

router = routers.DefaultRouter()

router.register(r"auth", AuthViewSet, basename="auth")
router.register(r"studies", StudyViewSet, basename="study")
router.register(r"datasets", DatasetViewSet, basename="dataset")
router.register(r"classify", ClassifyViewSet, basename="classify")
router.register(r"share", ShareViewSet, basename="share")
router.register(r"export", ExportViewSet, basename="export")

urlpatterns = router.urls
