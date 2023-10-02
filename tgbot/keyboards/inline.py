import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.text.user import get_price, get_price_rub


def get_right_price(price):
    return f'{price[0]} {price[1::]}'


telegram_support = os.environ.get("TELEGRAM_SUPPORT")
review_chat = os.environ.get("REVIEW_CHAT")
news_channel = os.environ.get("NEWS_CHANNEL")
mixer_bot = os.environ.get("MIXER_BOT")


def start_inline_user_keyboadr():
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    buy_btc = InlineKeyboardButton('👉🏻 Купить Биткоин 👈🏻', callback_data='Buy Bitcoin')
    promocode = InlineKeyboardButton('Промокод', callback_data="Promocode")
    help = InlineKeyboardButton('📖 Помощь', callback_data="Help Command")
    partner_programm = InlineKeyboardButton('👥 Партнерская программа', callback_data="Partner Programm")
    feedback = InlineKeyboardButton('📧 Обратная связь', callback_data="Feedback")
    support = InlineKeyboardButton('Поддержка / Оператор', url=f"https://t.me/{telegram_support}")
    review = InlineKeyboardButton('Отзывы', url=f"https://t.me/{review_chat}")
    news = InlineKeyboardButton('Новостной канал', url=f"https://t.me/{news_channel}")
    sell_btc = InlineKeyboardButton('Продать биткоин', callback_data="Sell Bitcoin")
    mixer = InlineKeyboardButton('⚡️BTC Mixer', url=f"https://t.me/{mixer_bot}")

    buttons \
        .add(buy_btc) \
        .add(promocode, help) \
        .add(partner_programm, feedback) \
        .add(support) \
        .add(review) \
        .add(news) \
        .add(sell_btc) \
        .add(mixer)

    return buttons


def partner_inline_user_keyboard():
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    partner_link = InlineKeyboardButton('🔗 Моя партнерская ссылка', callback_data='My partner link')
    my_finance = InlineKeyboardButton('📝 Мои финансы', callback_data="My finance")
    out_commission = InlineKeyboardButton('Вывод комиссионных (кошелек)', callback_data="Out commission")
    out_back = InlineKeyboardButton('💸 Вывод', callback_data="Outback")
    back = InlineKeyboardButton('НАЗАД', callback_data="Back Main Menu")

    buttons \
        .add(partner_link) \
        .add(my_finance, out_commission) \
        .add(out_back) \
        .add(back)

    return buttons


def cancel_inline_user_keyboard():
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    cancel = InlineKeyboardButton('🚫Отмена', callback_data="Cancel")

    buttons \
        .add(cancel)

    return buttons


def choose_pay_user_keyboard(price):
    if ',' in price:
        choose_amount = float(price.replace(',', '.'))
    else:
        choose_amount = float(price)
    if ',' in price or '.' in price:
        # Получаем курс BTC/RUB
        btc_rub = get_price('RUB')

        buttons = InlineKeyboardMarkup(resize_keyboard=True)
        sberbank = InlineKeyboardButton(
            f'Сбербанк ({round(float(btc_rub) * choose_amount)} руб.)',
            callback_data="Sberbank"
        )
        sberbank_moscow = InlineKeyboardButton(
            f'Сбербанк MOSCOW ({round(float(btc_rub) * choose_amount)} руб.)',
            callback_data="Sberbank"
        )
        sberbank_piter = InlineKeyboardButton(
            f'Сбербанк Питер ({round(float(btc_rub) * choose_amount)} руб.)',
            callback_data="Sberbank"
        )
        cards = InlineKeyboardButton(
            f'💳 Visa / MasterCard / МИР ({round(float(btc_rub) * choose_amount)}) руб.',
            callback_data="Visa|MasterCard|МИР"
        )
        cansel = InlineKeyboardButton('🚫Отмена', callback_data="Cancel")

        buttons \
            .add(sberbank) \
            .add(sberbank_moscow) \
            .add(sberbank_piter) \
            .add(cards) \
            .add(cansel)

        return buttons
    else:
        # choose_amount = get_price_rub(price)
        buttons = InlineKeyboardMarkup(resize_keyboard=True)
        sberbank = InlineKeyboardButton(
            f'Сбербанк ({price} руб.)',
            callback_data="Sberbank"
        )
        sberbank_moscow = InlineKeyboardButton(
            f'Сбербанк MOSCOW ({price} руб.)',
            callback_data="Sberbank"
        )
        sberbank_piter = InlineKeyboardButton(
            f'Сбербанк Питер ({price} руб.)',
            callback_data="Sberbank"
        )
        cards = InlineKeyboardButton(
            f'💳 Visa / MasterCard / МИР ({price}) руб.',
            callback_data="Visa|MasterCard|МИР"
        )
        cansel = InlineKeyboardButton('🚫Отмена', callback_data="Cancel")

        buttons \
            .add(sberbank) \
            .add(sberbank_moscow) \
            .add(sberbank_piter) \
            .add(cards) \
            .add(cansel)

        return buttons


def agree_pay_user_keyboard():
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    cancel = InlineKeyboardButton('🚫Отмена', callback_data="Cancel")
    agree_pay = InlineKeyboardButton('Согласен ✅', callback_data="Agree Pay")

    buttons \
        .add(cancel, agree_pay)

    return buttons
