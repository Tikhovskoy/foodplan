from aiogram import Router
from . import start  # сюда будем добавлять другие модули

def register_all_handlers(dp: Router):
    dp.include_router(start.router)