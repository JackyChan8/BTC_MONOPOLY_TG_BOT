from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

from tgbot.text.user import choose_method_pay, telegram_support
from tgbot.validate.validate import validate_form
from tgbot.keyboards.inline import partner_inline_user_keyboard, choose_pay_user_keyboard, agree_pay_user_keyboard

from database.database import add_wallet_user, add_amount_btc_wallet, get_amount_price


# =========================================== Кошелек для выплаты Комиссионых ======================================== #

class WalletCommission(StatesGroup):
    wallet = State()


class WalletShop(StatesGroup):
    wallet = State()


class AmountBitcoin(StatesGroup):
    amount = State()


async def get_text_wallet(message: types.Message, state: WalletCommission.wallet):
    async with state.proxy() as data:
        data['text'] = message.text

    # Add wallet to database
    await add_wallet_user(message.from_user.id, data['text'], 'referrel')

    # Возращаем сообщение пользователю
    text = f"""
Вы указали адрес {data['text']}.

Ваши партнерские вознаграждения будут отправленны на этот адрес по запросу, кнопка Вывод.
    """
    await message.answer(
        text,
        reply_markup=partner_inline_user_keyboard(),
        parse_mode='Markdown'
    )
    await state.finish()


async def get_text_wallet_buy(message: types.Message, state: WalletShop.wallet):
    async with state.proxy() as data:
        data['text'] = message.text

    res_valid = await validate_form('bitcoin_wallet', message)
    if res_valid:
        # Add wallet to database
        await add_wallet_user(message.from_user.id, data['text'], 'buy')
        amount_rub = await get_amount_price(message.from_user.id, 'amount_rub')
        # Возращаем сообщение пользователю
        text = f"""
*Время на оплату заказа 15 минут!*

```
ВАЖНО: При оплате НЕ ЗАПОЛНЯЙТЕ поле комментария платежа. Любые платежи с комментариями не будут обработаны ботом, а перечисленные средства не будут возвращены! Обращаем внимание: средства вы должны отправлять только со своей личной карты. Администрация может потребовать верификацию документов клиента или задержать обмен для проверки других данных. Средства отправленные без заявки, возврату не подлежат! Оплачивать вы должны ровно ту сумму, которая указана в заявке, иначе ваш платеж потеряется.  Все претензии по обмену принимаются в течении 24 часов.
```
Итого к оплате: *{amount_rub} руб.*

После оплаты средства будут переведены на кошелек: 
```
{data['text']}
```

Если у вас есть вопрос, или возникли проблемы с оплатой, пишите поддержке: @{telegram_support}

Вы согласны на обмен?
        """
        await message.delete()
        await message.answer(
            text,
            reply_markup=agree_pay_user_keyboard(),
            parse_mode='Markdown'
        )
        await state.finish()


async def get_amount(message: types.Message, state: AmountBitcoin.amount):
    async with state.proxy() as data:
        data['text'] = message.text

    res_valid = await validate_form('amount', message)
    if res_valid:
        # Add wallet to Amount
        await add_amount_btc_wallet(message.from_user.id, data['text'])

        # Возращаем сообщение пользователю
        text = await choose_method_pay(message.from_user.id)
        await message.answer(
            text,
            reply_markup=choose_pay_user_keyboard(data['text']),
            parse_mode='Markdown'
        )
        await state.finish()
