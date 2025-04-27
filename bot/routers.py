from aiogram import Dispatcher

from bot.handlers.greeting import router as greeting_router
from bot.handlers.subscription import router as subscription_router
from bot.handlers.meal_type import router as meal_type_router
from bot.handlers.diet import router as diet_router
from bot.handlers.budget import router as budget_router
from bot.handlers.show_recipes import router as show_recipes_router

def register_routers(dp: Dispatcher):
    dp.include_router(greeting_router)
    dp.include_router(subscription_router)
    dp.include_router(meal_type_router)
    dp.include_router(diet_router)
    dp.include_router(budget_router)
    dp.include_router(show_recipes_router)
