import random
from decimal import Decimal
from io import BytesIO

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils.translation import gettext as _
from PIL import Image, ImageDraw, ImageFont

from core.models import Category
from recipes.models import Recipe, Ingredient, RecipeIngredient


SAMPLE_CATEGORIES = [
    "Веган", "Без глютена", "Эконом", "Праздничное", "Быстрое"
]

SAMPLE_INGREDIENTS = [
    ("Картофель",     "pcs", Decimal("10.00")),
    ("Морковь",       "pcs", Decimal("5.00")),
    ("Лук",           "pcs", Decimal("3.00")),
    ("Куриное филе",  "g",   Decimal("0.20")),
    ("Рис",           "g",   Decimal("0.05")),
    ("Грибы",         "g",   Decimal("0.15")),
    ("Творог",        "g",   Decimal("0.12")),
    ("Мука",          "g",   Decimal("0.02")),
]

COMMAND_EXAMPLES = [
    {
        "title": "Быстрый картофельный суп",
        "categories": ["Быстрое", "Эконом"],
        "instructions": (
            "1. Очистить и нарезать картофель, морковь и лук.\n"
            "2. Залить овощи водой, довести до кипения.\n"
            "3. Варить 10–15 минут до готовности.\n"
            "4. Посолить, поперчить по вкусу и подавать горячим."
        ),
        "ingredients": [
            {"name": "Картофель", "amount": 5, "unit": "pcs"},
            {"name": "Морковь",   "amount": 1, "unit": "pcs"},
            {"name": "Лук",       "amount": 1, "unit": "pcs"},
        ],
    },
    {
        "title": "Грибное ризотто",
        "categories": ["Праздничное"],
        "instructions": (
            "1. На сковороде обжарить лук до прозрачности.\n"
            "2. Добавить рис и слегка обжарить.\n"
            "3. Постепенно вливать горячую воду, помешивая, пока рис не станет кремовым.\n"
            "4. В конце добавить грибы, перемешать и снять с огня."
        ),
        "ingredients": [
            {"name": "Рис",   "amount": 200, "unit": "g"},
            {"name": "Грибы", "amount": 150, "unit": "g"},
            {"name": "Лук",   "amount": 1,   "unit": "pcs"},
        ],
    },
    {
        "title": "Морковный салат",
        "categories": ["Веган", "Эконом", "Быстрое"],
        "instructions": (
            "1. Натереть морковь на крупной тёрке.\n"
            "2. Добавить мелко нарезанный лук.\n"
            "3. Заправить растительным маслом, посолить и перемешать."
        ),
        "ingredients": [
            {"name": "Морковь", "amount": 3, "unit": "pcs"},
            {"name": "Лук",     "amount": 1, "unit": "pcs"},
        ],
    },
    {
        "title": "Картофельное пюре",
        "categories": ["Эконом", "Быстрое"],
        "instructions": (
            "1. Отварить картофель до мягкости.\n"
            "2. Слить воду, растолочь картофель.\n"
            "3. Добавить поджаренный лук, посолить, перемешать."
        ),
        "ingredients": [
            {"name": "Картофель", "amount": 4, "unit": "pcs"},
            {"name": "Лук",       "amount": 1, "unit": "pcs"},
        ],
    },
    {
        "title": "Овощное рагу",
        "categories": ["Веган", "Эконом"],
        "instructions": (
            "1. Нарезать картофель, морковь, грибы и лук.\n"
            "2. В сотейнике обжарить лук, добавить остальные овощи.\n"
            "3. Тушить под крышкой 15–20 минут, посолить."
        ),
        "ingredients": [
            {"name": "Картофель", "amount": 2,   "unit": "pcs"},
            {"name": "Морковь",   "amount": 2,   "unit": "pcs"},
            {"name": "Грибы",     "amount": 100, "unit": "g"},
            {"name": "Лук",       "amount": 1,   "unit": "pcs"},
        ],
    },
    {
        "title": "Рисовая каша",
        "categories": ["Эконом"],
        "instructions": (
            "1. Промыть рис.\n"
            "2. Сварить рис в воде до готовности, посолить по вкусу.\n"
            "3. При желании добавить сливочное масло."
        ),
        "ingredients": [
            {"name": "Рис", "amount": 150, "unit": "g"},
        ],
    },
    {
        "title": "Куриный плов",
        "categories": ["Праздничное"],
        "instructions": (
            "1. Обжарить лук и морковь до золотистого цвета.\n"
            "2. Добавить рис и куриное филе, залить водой.\n"
            "3. Тушить под крышкой 20–25 минут, посолить."
        ),
        "ingredients": [
            {"name": "Рис",          "amount": 200, "unit": "g"},
            {"name": "Куриное филе", "amount": 200, "unit": "g"},
            {"name": "Лук",          "amount": 1,   "unit": "pcs"},
            {"name": "Морковь",      "amount": 1,   "unit": "pcs"},
        ],
    },
    {
        "title": "Грибное соте",
        "categories": ["Праздничное", "Быстрое"],
        "instructions": (
            "1. Нарезать грибы и лук.\n"
            "2. Обжарить лук, добавить грибы и готовить 5–7 минут.\n"
            "3. Посолить и подавать горячим."
        ),
        "ingredients": [
            {"name": "Грибы", "amount": 200, "unit": "g"},
            {"name": "Лук",   "amount": 1,   "unit": "pcs"},
        ],
    },
    {
        "title": "Творожные оладьи",
        "categories": ["Праздничное"],
        "instructions": (
            "1. Смешать творог с мукой до однородности.\n"
            "2. Смажьте сковороду маслом, выпекайте оладьи по 2 минуты с каждой стороны."
        ),
        "ingredients": [
            {"name": "Творог", "amount": 200, "unit": "g"},
            {"name": "Мука",   "amount": 50,  "unit": "g"},
        ],
    },
    {
        "title": "Картофельные оладьи",
        "categories": ["Эконом", "Быстрое"],
        "instructions": (
            "1. Натереть картофель и лук, отжать лишний сок.\n"
            "2. Смешать с мукой и сформировать оладьи.\n"
            "3. Обжарить до золотистой корочки."
        ),
        "ingredients": [
            {"name": "Картофель", "amount": 3,  "unit": "pcs"},
            {"name": "Мука",      "amount": 50, "unit": "g"},
            {"name": "Лук",       "amount": 1,  "unit": "pcs"},
        ],
    },
    {
        "title": "Рис с грибами",
        "categories": ["Эконом", "Без глютена"],
        "instructions": (
            "1. Обжарить грибы и лук.\n"
            "2. Добавить рис, залить водой и варить до готовности.\n"
            "3. Посолить и подавать."
        ),
        "ingredients": [
            {"name": "Рис",   "amount": 150, "unit": "g"},
            {"name": "Грибы", "amount": 100, "unit": "g"},
        ],
    },
    {
        "title": "Куриное филе с грибами",
        "categories": ["Праздничное", "Без глютена"],
        "instructions": (
            "1. Обжарить куриное филе до золотистого цвета.\n"
            "2. Добавить грибы и готовить ещё 5–7 минут.\n"
            "3. Посолить и подавать с гарниром."
        ),
        "ingredients": [
            {"name": "Куриное филе", "amount": 200, "unit": "g"},
            {"name": "Грибы",        "amount": 150, "unit": "g"},
        ],
    },
    {
        "title": "Постный суп",
        "categories": ["Веган", "Эконом"],
        "instructions": (
            "1. Нарезать картофель и морковь.\n"
            "2. Вскипятить воду, добавить овощи и варить 10–15 минут.\n"
            "3. Посолить и подавать горячим."
        ),
        "ingredients": [
            {"name": "Картофель", "amount": 3, "unit": "pcs"},
            {"name": "Морковь",   "amount": 2, "unit": "pcs"},
        ],
    },
    {
        "title": "Быстрый гарнир из моркови",
        "categories": ["Быстрое", "Эконом"],
        "instructions": (
            "1. Морковь нарезать брусками и обжарить 5 минут.\n"
            "2. Посолить и подавать как гарнир."
        ),
        "ingredients": [
            {"name": "Морковь", "amount": 3, "unit": "pcs"},
        ],
    },
    {
        "title": "Грибной суп",
        "categories": ["Эконом", "Без глютена"],
        "instructions": (
            "1. Нарезать грибы, лук и картофель.\n"
            "2. Отварить овощи до готовности, добавить грибы за 5 минут до конца.\n"
            "3. Посолить и подавать."
        ),
        "ingredients": [
            {"name": "Грибы",     "amount": 150, "unit": "g"},
            {"name": "Картофель", "amount": 2,   "unit": "pcs"},
            {"name": "Лук",       "amount": 1,   "unit": "pcs"},
        ],
    },
    {
        "title": "Куриный бульон",
        "categories": ["Без глютена"],
        "instructions": (
            "1. Залить куриное филе водой и довести до кипения.\n"
            "2. Варить 20–25 минут, убрать пену, посолить.\n"
            "3. Подавать с зеленью."
        ),
        "ingredients": [
            {"name": "Куриное филе", "amount": 300, "unit": "g"},
            {"name": "Лук",           "amount": 1,   "unit": "pcs"},
        ],
    },
    {
        "title": "Рисовый плов",
        "categories": ["Праздничное"],
        "instructions": (
            "1. Обжарить морковь и лук до мягкости.\n"
            "2. Добавить рис, залить водой и тушить 20 минут.\n"
            "3. Посолить и подавать горячим."
        ),
        "ingredients": [
            {"name": "Рис",      "amount": 200, "unit": "g"},
            {"name": "Морковь",  "amount": 1,   "unit": "pcs"},
            {"name": "Лук",      "amount": 1,   "unit": "pcs"},
        ],
    },
    {
        "title": "Творожная запеканка",
        "categories": ["Праздничное"],
        "instructions": (
            "1. Смешать творог с мукой до пасты.\n"
            "2. Выложить в форму и запечь при 180°C 25–30 минут."
        ),
        "ingredients": [
            {"name": "Творог", "amount": 300, "unit": "g"},
            {"name": "Мука",   "amount": 50,  "unit": "g"},
        ],
    },
    {
        "title": "Картофель во фритюре",
        "categories": ["Эконом", "Быстрое"],
        "instructions": (
            "1. Нарезать картофель ломтиками.\n"
            "2. Обжарить во фритюре или в глубокой кастрюле с маслом до хрустящей корочки."
        ),
        "ingredients": [
            {"name": "Картофель", "amount": 4, "unit": "pcs"},
        ],
    },
    {
        "title": "Курино-рисовый салат",
        "categories": ["Праздничное", "Без глютена", "Быстрое"],
        "instructions": (
            "1. Отварить куриное филе и рис, остудить.\n"
            "2. Нарезать филе кубиками и смешать с рисом.\n"
            "3. Добавить мелко нарезанный лук, заправить маслом и посолить."
        ),
        "ingredients": [
            {"name": "Куриное филе", "amount": 150, "unit": "g"},
            {"name": "Рис",           "amount": 100, "unit": "g"},
            {"name": "Лук",           "amount": 1,   "unit": "pcs"},
        ],
    },
]

class Command(BaseCommand):
    help = _("Заполняет базу тестовыми рецептами с категориями, ингредиентами, инструкциями и placeholder-картинками")

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(_("Создаём справочник категорий…"))
        category_objs = {
            name: Category.objects.get_or_create(name=name)[0]
            for name in SAMPLE_CATEGORIES
        }

        self.stdout.write(_("Создаём справочник ингредиентов…"))
        for name, _, _ in SAMPLE_INGREDIENTS:
            Ingredient.objects.get_or_create(name=name)
        cost_map = {(n, u): c for n, u, c in SAMPLE_INGREDIENTS}

        # Попытка загрузить кириллический шрифт, иначе дефолт
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=24)
        except IOError:
            font = ImageFont.load_default()

        self.stdout.write(_("🍽 Стадим рецепты…"))
        for data in COMMAND_EXAMPLES:
            title = data["title"]
            instr = data["instructions"]
            cats  = [category_objs[n] for n in data["categories"]]

            rec, created = Recipe.objects.get_or_create(
                title=title,
                defaults={"estimated_cost": Decimal("0.00"), "instructions": instr}
            )
            # обновляем инструкцию, если она изменилась
            if not created and rec.instructions != instr:
                rec.instructions = instr
                rec.save(update_fields=["instructions"])

            rec.categories.set(cats)

            # чистим старые ингредиенты и создаём новые
            RecipeIngredient.objects.filter(recipe=rec).delete()
            total = Decimal("0.00")
            for item in data["ingredients"]:
                ing_obj = Ingredient.objects.get(name=item["name"])
                amount  = Decimal(str(item["amount"]))
                cost    = cost_map[(item["name"], item["unit"])]
                RecipeIngredient.objects.create(
                    recipe=rec,
                    ingredient=ing_obj,
                    amount=amount,
                    unit=item["unit"],
                    unit_cost=cost
                )
                total += amount * cost

            # сохраняем рассчитанную стоимость
            rec.estimated_cost = total
            rec.save(update_fields=["estimated_cost"])

            # Генерируем placeholder-изображение и сохраняем его под именем "<pk>.jpg"
            buf = BytesIO()
            img = Image.new("RGB", (600, 400), (230, 230, 230))
            draw = ImageDraw.Draw(img)
            bbox = draw.textbbox((0, 0), title, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text(
                ((600 - w) / 2, (400 - h) / 2),
                title,
                fill=(30, 30, 30),
                font=font
            )
            img.save(buf, format="JPEG", quality=80)
            # имя файла — просто номер записи
            filename = f"{rec.pk}.jpg"
            rec.image.save(filename, ContentFile(buf.getvalue()), save=True)

            self.stdout.write(f"  • {title} → {total}₽")

        self.stdout.write(self.style.SUCCESS(_("✅ Все рецепты созданы")))
