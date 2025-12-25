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
    except (ValueError, TypeError, AttributeError) as e:
        return JsonResponse({"detail": f"Invalid payload: {str(e)}"}, status=400)
    except Exception as e:
        return JsonResponse({"detail": f"Invalid request: {str(e)}"}, status=400)

    try:
        features = {"size": size, "bedrooms": bedrooms, "age": age}
        price = predict_price(features)
        PredictionLog.objects.create(payload=features, predicted_price=price)
        return JsonResponse({"predicted_price": price})
    except FileNotFoundError as e:
        return JsonResponse(
            {"detail": "Model not trained yet. Please train the model first."}, 
            status=503
        )
    except Exception as e:
        return JsonResponse(
            {"detail": f"Prediction failed: {str(e)}"}, 
            status=500
        )


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
