from django.db import models

from django.db import models


class TrainingRun(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    dataset_rows = models.IntegerField()
    r2_score = models.FloatField()
    mae = models.FloatField()
    model_path = models.CharField(max_length=255)

    class Meta:
        ordering = ["-created_at"]


class PredictionLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    payload = models.JSONField()
    predicted_price = models.FloatField()

    class Meta:
        ordering = ["-created_at"]


