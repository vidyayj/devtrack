from django.urls import path
from . import views

urlpatterns = [
    path("health/", views.health),
    path("reporters/", views.reporters),
    path("issues/", views.issues),
]