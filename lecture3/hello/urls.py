from django.urls import path
from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("nicolas", views.nicolas, name="nicolas"),
  path('<str:name>', views.greet, name="greet")
]