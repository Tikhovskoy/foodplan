import json
import logging

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from telegram import Bot, Update
# from telegram.utils.request import Request

# from .handlers import handle_update

logger = logging.getLogger(__name__)

def health(request):
    """
    Простой эндпоинт для проверки, что сервис жив.
    """
    return JsonResponse({'status': 'ok'})

@csrf_exempt
def telegram_webhook(request, token):
    """
    Webhook для приёма обновлений от Telegram.
    URL: /webhook/<token>/
    """
    if token != settings.TELEGRAM_TOKEN:
        return HttpResponse(status=403)

    if request.method != 'POST':
        return HttpResponse(status=405)

    try:
        payload = json.loads(request.body.decode('utf-8'))
        bot = Bot(settings.TELEGRAM_TOKEN, request=Request())
        update = Update.de_json(payload, bot)
        # handle_update(update)
    except Exception as e:
        logger.error(f"Webhook handling error: {e}", exc_info=True)

    return HttpResponse(status=200)
