from users.models import User, Profile
from asgiref.sync import sync_to_async

class ProfileService:
    @sync_to_async
    def get_or_create_profile(self, telegram_id):
        user, _ = User.objects.get_or_create(telegram_id=telegram_id)
        Profile.objects.get_or_create(user=user)

profile_service = ProfileService()
