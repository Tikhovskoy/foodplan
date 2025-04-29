from users.models import TelegramUser


class UserService:
    async def get_or_create_user(self, telegram_id: int, username: str = "", first_name: str = "", last_name: str = ""):
        return await TelegramUser.objects.aupdate_or_create(
            telegram_id=telegram_id,
            defaults={
                "username": username or f"user_{telegram_id}",
                "first_name": first_name,
                "last_name": last_name
            }
        )
