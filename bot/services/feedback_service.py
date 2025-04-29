from feedback.models import Feedback


class FeedbackService:
    async def create_feedback(self, telegram_id: int, text: str):
        return await Feedback.objects.acreate(telegram_id=telegram_id, text=text)
