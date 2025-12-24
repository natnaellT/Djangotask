from celery import shared_task
from django.db import transaction

from .models import TrainingRun
from .ml.pipeline import train_and_evaluate


@shared_task
def retrain_model_task():
    metrics = train_and_evaluate()
    with transaction.atomic():
        TrainingRun.objects.create(
            dataset_rows=metrics["rows"],
            r2_score=metrics["r2"],
            mae=metrics["mae"],
            model_path=metrics["model_path"],
        )
    return metrics