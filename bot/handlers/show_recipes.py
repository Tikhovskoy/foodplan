from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.services.recipe_service import recipe_service
from bot.services.subscription_service import subscription_service
from bot.keyboards.reply import (
    get_recipe_main_kb, 
    get_step_navigation_kb, 
    get_buy_subscription_kb, 
    get_back_to_recipe_kb
)
from bot.states import RecipeStepStates, SubscriptionStates
from bot.logic.exceptions import RecipeNotFound
from bot.shared.send_tools import send_recipe


router = Router()

@router.message()
async def send_recipes(message: Message, state: FSMContext):
    try:
        recipe = await recipe_service.fetch_random(message.from_user.id)

        await state.clear()
        await state.update_data(recipe_id=recipe.id, step_index=0)

        caption = f"🍽 Ваш рецепт:\n\n📓 {recipe.title}"

        await send_recipe(message, caption, recipe.image, reply_markup=get_recipe_main_kb(recipe.id))

    except RecipeNotFound as e:
        await message.answer(str(e))
        await state.clear()
    except Exception as e:
        print(f"Error in send_recipes: {e}")
        await message.answer("⚠️ Произошла ошибка при получении рецепта.")
        await state.clear()

@router.callback_query(F.data.startswith("show_steps_"))
async def start_steps(callback: CallbackQuery, state: FSMContext):
    try:
        recipe_id = int(callback.data.split("_")[2])
        steps = await recipe_service.get_steps(recipe_id)

        if not steps:
            await callback.message.answer("⚠️ Нет шагов приготовления для этого рецепта.")
            return

        await state.update_data(recipe_id=recipe_id, step_index=0)
        await show_step(
            callback.message,
            step=steps[0],
            current_step=1,
            total_steps=len(steps),
            show_next_button=len(steps) > 1
        )
    except RecipeNotFound as e:
        await callback.message.answer(str(e))
    except Exception as e:
        print(f"Error in start_steps: {e}")
        await callback.message.answer("⚠️ Произошла ошибка при получении шагов рецепта.")

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

        await show_step(
            callback.message,
            step=steps[next_index],
            current_step=next_index + 1,
            total_steps=len(steps),
            show_next_button=show_next_button,
            recipe_id=recipe_id
        )
    except Exception as e:
        print(f"Error in next_step: {e}")
        await callback.message.answer("⚠️ Произошла ошибка при переходе к следующему шагу.")


async def show_step(message: Message, step, current_step: int, total_steps: int, show_next_button=True, recipe_id=None):
    text = f"Шаг {current_step}/{total_steps}:\n\n{step.text}"

    if current_step == total_steps:
        reply_markup = get_back_to_recipe_kb(recipe_id)
    else:
        reply_markup = get_step_navigation_kb()

    await send_recipe(
        message,
        caption=text,
        image_field=step.image,
        reply_markup=reply_markup
    )

@router.callback_query(F.data.startswith("back_to_recipe_"))
async def back_to_recipe(callback: CallbackQuery, state: FSMContext):
    try:
        recipe_id = int(callback.data.split("_")[3])
        recipe = await recipe_service._recipes.get(recipe_id)

        caption = f"🍽 Ваш рецепт:\n\n📓 {recipe.title}"
        await send_recipe(
            callback.message,
            caption=caption,
            image_field=recipe.image,
            reply_markup=get_recipe_main_kb(recipe.id)
        )
        await callback.answer()
    except Exception as e:
        print(f"Ошибка при возврате к рецепту: {e}")
        await callback.message.answer("⚠️ Ошибка при возврате к рецепту.")

@router.callback_query(F.data == "next_recipe")
async def next_recipe(callback: CallbackQuery, state: FSMContext):
    try:
        user_id = callback.from_user.id
        is_active = await subscription_service.check_active(user_id)

        if is_active:
            await send_recipes(callback.message, state)
        else:
            await callback.message.answer(
                "🔒 Для просмотра дополнительных рецептов требуется подписка.\nХотите оформить подписку?",
                reply_markup=get_buy_subscription_kb()
            )
            await state.set_state(SubscriptionStates.waiting_for_subscription_choice)
    except Exception as e:
        print(f"Error in next_recipe: {e}")
        await callback.message.answer("⚠️ Произошла ошибка при запросе нового рецепта.")

@router.callback_query(F.data.startswith("ingredients_"))
async def show_ingredients(callback: CallbackQuery):
    try:
        recipe_id = int(callback.data.split("_")[1])
        ingredients = await recipe_service.get_ingredients(recipe_id)

        if ingredients:
            text_lines = []
            for name, data in ingredients.items():
                line = f"- {name} — {data['amount']} {data['unit']}"
                text_lines.append(line)

            text = "\n".join(text_lines)
            await callback.message.answer(f"🛒 Ингредиенты:\n{text}")
        else:
            await callback.message.answer("⚠️ У этого рецепта нет ингредиентов.")
    except Exception as e:
        print(f"Ошибка при получении ингредиентов: {e}")
        await callback.message.answer("⚠️ Ошибка при получении ингредиентов.")


@router.callback_query(F.data.startswith("dislike_"))
async def dislike_recipe(callback: CallbackQuery, state: FSMContext):
    try:
        recipe_id = int(callback.data.split("_")[1])
        await recipe_service.save_dislike(callback.from_user.id, recipe_id)
        await callback.answer("👎 Рецепт больше не будет показываться!")

        user_id = callback.from_user.id
        is_active = await subscription_service.check_active(user_id)

        if is_active:
            await send_recipes(callback.message, state)
        else:
            await callback.message.answer(
                "🔒 Для просмотра дополнительных рецептов требуется подписка.\nХотите оформить подписку?",
                reply_markup=get_buy_subscription_kb()
            )
            await state.set_state(SubscriptionStates.waiting_for_subscription_choice)
    except Exception as e:
        print(f"Error in dislike_recipe: {e}")
        await callback.message.answer("⚠️ Произошла ошибка при сохранении предпочтений.")