from app.views.auth import AuthViewSet
from app.views.classify import ClassifyViewSet
from app.views.dataset import DatasetViewSet
from app.views.share import ShareViewSet
from app.views.study import StudyViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r"auth", AuthViewSet, basename="auth")
router.register(r"studies", StudyViewSet, basename="study")
router.register(r"share", ShareViewSet, basename="share")
router.register(r"datasets", DatasetViewSet, basename="dataset")
router.register(r"classify", ClassifyViewSet, basename="classify")

urlpatterns = router.urls
