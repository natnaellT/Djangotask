import json
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

from .models import TrainingRun, PredictionLog
from .ml.pipeline import predict_price
from .tasks import retrain_model_task


@csrf_exempt
def predict_price_view(request):
    if request.method != "POST":
        return JsonResponse({"detail": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        size = float(data.get("size"))
        bedrooms = float(data.get("bedrooms"))
        age = float(data.get("age"))
    except Exception:
        return JsonResponse({"detail": "Invalid payload"}, status=400)

    features = {"size": size, "bedrooms": bedrooms, "age": age}
    price = predict_price(features)

    PredictionLog.objects.create(payload=features, predicted_price=price)

    return JsonResponse({"predicted_price": price})


def model_status(request):
    last_run = TrainingRun.objects.first()
    if not last_run:
        return JsonResponse({"trained": False})

    return JsonResponse(
        {
            "trained": True,
            "last_trained_at": last_run.created_at.isoformat(),
            "rows": last_run.dataset_rows,
            "r2": last_run.r2_score,
            "mae": last_run.mae,
        }
    )


@csrf_exempt
def trigger_training(request):
    if request.method != "POST":
        return JsonResponse({"detail": "Only POST allowed"}, status=405)

    retrain_model_task.delay()
    return JsonResponse({"detail": "Training started"}, status=202)
