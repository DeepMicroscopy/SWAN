from django.urls import path

from . import views

urlpatterns = [
    path("studies/", views.index_studies, name="index-studies"),
    path("studies/<uuid>", views.study, name="study"),
    path("studies/<uuid>/image", views.study_image, name="study-image"),
]