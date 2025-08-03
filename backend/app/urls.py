from django.urls import path

from . import views

urlpatterns = [
    path("classify/", views.classify),

    path("studies/", views.index_studies, name="index-studies"),
    path("studies/<uuid>", views.study, name="study"),
    path("studies/<uuid>/image", views.study_image, name="study-image"),
    path("studies/<uuid>/index", views.study_index, name="study-index"),
    path("studies/<uuid>/<int:index>", views.study_entry, name="study-entry"),

    path("datasets/", views.index_datasets, name="index-datasets"),
    path("datasets/<uuid>", views.dataset, name="dataset"),
    path("datasets/<uuid>/<index>", views.dataset_image, name="dataset-image"),
]