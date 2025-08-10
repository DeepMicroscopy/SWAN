from rest_framework import routers

from .auth import AuthViewSet
from .classify import ClassifyViewSet
from .dataset import DatasetViewSet
from .study import StudyViewSet

router = routers.DefaultRouter()

router.register(r"auth", AuthViewSet, basename="auth")
router.register(r"studies", StudyViewSet, basename="study")
router.register(r"datasets", DatasetViewSet, basename="dataset")
router.register(r"classify", ClassifyViewSet, basename="classify")

urlpatterns = router.urls
