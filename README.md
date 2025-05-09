# FoodPlan

**FoodPlan** — Telegram-бот с Django-бэкендом и админкой. Он помогает пользователю:
- подобрать рецепты по времени приёма пищи и категории;
- листать рецепты по предпочтениям без повторов;
- просматривать пошаговые инструкции и ингредиенты;
- получить подписку через Telegram-инвойс и открыть доступ ко всем функциям.

---

## Функциональность

- Выбор **времени приёма пищи** и **категории рецепта** через inline-кнопки;
- Получение рецепта, пошаговой инструкции и списка ингредиентов;
- Ограничение на 1 рецепт в день без подписки;
- Telegram-инвойсы для оплаты подписки;
- Управление рецептами, категориями, временем приёма пищи и подписками через Django-админку;
- Удобное возвращение в меню и перезапуск подбора рецептов;
- Все предпочтения сохраняются на уровне сессии бота.

---

## Текущая структура проекта

```text
foodplan/
├── bot/
│   ├── handlers/         # Все хендлеры бота (рецепты, подписка, категории и т.д.)
│   ├── keyboards/        # Кнопки (inline и reply)
│   ├── logic/            # Простая логика (например, исключения)
│   ├── shared/           # Общие функции: отправка фото, логгирование и т.д.
│   ├── main.py           # Запуск Telegram-бота
│   └── routers.py        # Регистрация всех маршрутов
├── recipes/              # Приложение с моделями рецептов, категорий, шагов, ингредиентов
├── users/                # TelegramUser и связанные данные
├── payments/             # SubscriptionPlan, Subscription, оплата
├── foodplan/             # Настройки Django
├── static/               # Статика проекта (опционально)
├── requirements.txt      # Зависимости проекта
├── .env                  # Конфигурация окружения (payment_token, DEBUG и т.д.)
└── manage.py             # Django CLI
````

---

## Как развернуть проект

```bash
git clone https://github.com/your-team/foodplan.git
cd foodplan

python3.8 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Настройка базы данных и админки
python manage.py migrate
python manage.py createsuperuser

# Запуск сервера и бота
python manage.py runserver
python bot/main.py
```

*Не забудьте создать `.env` с содержимым:*

```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
payment_token=your-token
ALLOWED_HOSTS=127.0.0.1,localhost
```

---

## Как оплатить подписку
1. Оплата осуществляется только в приложении, web-версия не позволяет проводить платежи.
2. Нажмите «💳 Оформить подписку» в Telegram.
3. Выберите тариф из админки.
4. Оплатите через Telegram-инвойс.
5. После успешной оплаты подписка активируется автоматически.

---

## Поддержка

По вопросам запуска и настройки — пишите.
