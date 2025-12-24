from django.urls import path
from . import views

urlpatterns = [
    path("predict/", views.predict_price_view, name="predict_price"),
    path("status/", views.model_status, name="model_status"),
    path("train/", views.trigger_training, name="trigger_training"),
]