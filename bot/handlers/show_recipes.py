from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from bot.services.recipe_service import recipe_service
from bot.shared.send_tools import send_recipe
from bot.keyboards.reply import (
    get_recipe_main_kb,
    get_back_to_recipe_kb,
    get_step_navigation_kb,
    get_restart_kb,
)
from bot.logic.exceptions import RecipeNotFound
from bot.keyboards.reply import get_meal_type_kb

router = Router()


@router.callback_query(F.data == "next_recipe")
async def next_recipe(callback: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        recipe_ids = data.get("recipe_ids", [])
        current_index = data.get("current_index", 0)

        if not recipe_ids:
            await callback.message.answer(
                "⚠️ Предпочтения не заданы или рецепты не загружены.",
                reply_markup=get_restart_kb()
            )
            return

        if current_index >= len(recipe_ids):
            await callback.message.answer(
                "😔 Кажется, рецепты по вашим предпочтениям закончились.",
                reply_markup=get_restart_kb()
            )
            return

        recipe_id = recipe_ids[current_index]
        recipe = await recipe_service.get_recipe(recipe_id)

        if not recipe:
            await callback.message.answer("⚠️ Рецепт не найден.")
            return

        caption = f"📖 {recipe.title}"
        if recipe.description:
            caption += f"\n\n📝 {recipe.description}"

        await send_recipe(
            callback.message,
            caption=caption,
            image_field=recipe.image,
            reply_markup=get_recipe_main_kb(recipe.id)
        )

        await state.update_data(current_index=current_index + 1)

    except Exception as e:
        print(f"Error in next_recipe: {e}")
        await callback.message.answer("⚠️ Произошла ошибка при показе следующего рецепта.")



@router.callback_query(F.data == "back_to_main_menu")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        "🏠 Вы вернулись в меню.\n\nПожалуйста, выберите время приёма пищи:",
        reply_markup=await get_meal_type_kb()
    )


@router.callback_query(F.data.startswith("show_steps_"))
async def start_steps(callback: CallbackQuery, state: FSMContext):
    try:
        recipe_id = int(callback.data.split("_")[2])
        steps = await recipe_service.get_steps(recipe_id)

        if not steps:
            await callback.message.answer("⚠️ Нет шагов приготовления для этого рецепта.")
            return

        await state.update_data(recipe_id=recipe_id, step_index=0)
        await show_step(callback.message, steps[0], 1, len(steps), show_next_button=len(steps) > 1, recipe_id=recipe_id)
    except RecipeNotFound as e:
        await callback.message.answer(str(e))
    except Exception as e:
        print(f"Error in start_steps: {e}")
        await callback.message.answer("⚠️ Ошибка при получении шагов рецепта.")


@router.callback_query(F.data == "next_step")
async def next_step(callback: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        recipe_id = data.get("recipe_id")
        step_index = data.get("step_index", 0)

        steps = await recipe_service.get_steps(recipe_id)
        next_index = step_index + 1

        if next_index >= len(steps):
            await callback.message.answer(
                "🎉 Все шаги пройдены! Приятного аппетита!",
                reply_markup=get_back_to_recipe_kb(recipe_id)
            )
            await state.clear()
            return

        await state.update_data(step_index=next_index)
        show_next_button = (next_index + 1) < len(steps)
        await show_step(callback.message, steps[next_index], next_index + 1, len(steps), show_next_button, recipe_id)
    except Exception as e:
        print(f"Error in next_step: {e}")
        await callback.message.answer("⚠️ Ошибка при переходе к следующему шагу.")


async def show_step(message, step, current_step, total_steps, show_next_button=True, recipe_id=None):
    text = f"Шаг {current_step}/{total_steps}:\n\n{step.text}"
    markup = get_step_navigation_kb() if show_next_button else get_back_to_recipe_kb(recipe_id)
    await send_recipe(message, caption=text, image_field=step.image, reply_markup=markup)


@router.callback_query(F.data.startswith("back_to_recipe_"))
async def back_to_recipe(callback: CallbackQuery, state: FSMContext):
    try:
        recipe_id = int(callback.data.split("_")[3])
        recipe = await recipe_service.get_recipe(recipe_id)
        caption = f"🍽 Ваш следующий рецепт:\n\n📓 {recipe.title}\n\n📝 {recipe.description}"
        await send_recipe(callback.message, caption, recipe.image, reply_markup=get_recipe_main_kb(recipe.id))
        await callback.answer()
    except Exception as e:
        print(f"Ошибка при возврате к рецепту: {e}")
        await callback.message.answer("⚠️ Ошибка при возврате к рецепту.")


@router.callback_query(F.data.startswith("ingredients_"))
async def show_ingredients(callback: CallbackQuery):
    try:
        recipe_id = int(callback.data.split("_")[1])
        ingredients = await recipe_service.get_ingredients(recipe_id)
        if not ingredients:
            await callback.message.answer("⚠️ У этого рецепта нет ингредиентов.")
            return

        text = "\n".join([
            f"- {name} — {data['amount']} {data['unit']}"
            for name, data in ingredients.items()
        ])
        await callback.message.answer(f"🛒 Ингредиенты:\n{text}")
    except Exception as e:
        print(f"Ошибка при получении ингредиентов: {e}")
        await callback.message.answer("⚠️ Ошибка при получении ингредиентов.")


@router.callback_query(F.data.startswith("dislike_"))
async def dislike_recipe(callback: CallbackQuery, state: FSMContext):
    try:
        recipe_id = int(callback.data.split("_")[1])
        await recipe_service.save_dislike(callback.from_user.id, recipe_id)
        await callback.answer("👎 Рецепт больше не будет показываться!")
        await next_recipe(callback, state)
    except Exception as e:
        print(f"Error in dislike_recipe: {e}")
        await callback.message.answer("⚠️ Ошибка при сохранении предпочтений.")
