from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.services.recipe_service import recipe_service
from bot.shared.send_tools import send_recipe
from bot.keyboards.reply import get_recipe_main_kb

router = Router()

@router.callback_query(F.data.startswith("category_"))
async def handle_category(callback: CallbackQuery, state: FSMContext):
    try:
        category_id = int(callback.data.replace("category_", ""))
        await state.update_data(category_id=category_id)

        data = await state.get_data()
        meal_time_id = data.get("meal_time_id")

        if not meal_time_id or not category_id:
            await callback.message.answer("⚠️ Пожалуйста, сначала выберите время приёма пищи и категорию.")
            return

        recipes = await recipe_service.fetch_all_by_meal_and_category(meal_time_id, category_id)
        if not recipes:
            await callback.message.answer("😔 К сожалению, рецептов по вашему запросу не найдено.")
            await state.clear()
            return

        recipe_ids = [r.id for r in recipes]
        await state.update_data(recipe_ids=recipe_ids, current_index=1)

        first_recipe = recipes[0]
        caption = f"🍽 Ваш рецепт:\n\n📓 {first_recipe.title}\n\n📝 {first_recipe.description}"
        await send_recipe(callback.message, caption, first_recipe.image, reply_markup=get_recipe_main_kb(first_recipe.id))

    except Exception as e:
        print(f"Error in handle_category: {e}")
        await callback.message.answer("⚠️ Произошла ошибка при выборе категории.")
