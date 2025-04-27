import os
from aiogram.types import FSInputFile
from django.conf import settings

async def send_recipe(message, caption: str, image_field, reply_markup=None):
    if image_field and hasattr(image_field, 'url') and image_field.name:
        local_path = os.path.join(settings.MEDIA_ROOT, image_field.name)
        if os.path.exists(local_path):
            photo = FSInputFile(local_path)
            await message.answer_photo(
                photo,
                caption=caption,
                reply_markup=reply_markup
            )
            return
        elif image_field.url and image_field.url.startswith("http"):
            await message.answer_photo(
                image_field.url,
                caption=caption,
                reply_markup=reply_markup
            )
            return
    await message.answer(
        caption,
        reply_markup=reply_markup
    )
