from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

from tgbot.text.admin import start_text
from tgbot.keyboards.reply_admin import start_admin_keyboard
from tgbot.validate.validate import validate_form
from database.database import update_wallet


# =========================================== Изменение Кошельков =========================================== #

class CardNumberSberbank(StatesGroup):
    card_number = State()


class CardNumberVISA(StatesGroup):
    card_number = State()


async def get_text_sberbank(message: types.Message, state: CardNumberSberbank.card_number):
    async with state.proxy() as data:
        data['text'] = message.text

    if message.text == "❌ Отменить":
        await state.finish()
        await message.answer(start_text, reply_markup=start_admin_keyboard())
    else:
        res_valid = await validate_form('card_number', message)
        if res_valid:
            # Add wallet to database
            await update_wallet('sberbank', data['text'])
            # Возращаем сообщение пользователю
            await message.reply(
                "🎉 Номер Банковской Карты успешно изменен!",
                reply_markup=start_admin_keyboard()
            )
            await state.finish()


async def get_text_visa(message: types.Message, state: CardNumberVISA.card_number):
    async with state.proxy() as data:
        data['text'] = message.text

    if message.text == "❌ Отменить":
        await state.finish()
        await message.answer(start_text, reply_markup=start_admin_keyboard())
    else:
        res_valid = await validate_form('card_number', message)
        if res_valid:
            # Add wallet to database
            await update_wallet('card', data['text'])
            # Возращаем сообщение пользователю
            await message.reply(
                "🎉 Номер Банковской Карты успешно изменен!",
                reply_markup=start_admin_keyboard()
            )
            await state.finish()
