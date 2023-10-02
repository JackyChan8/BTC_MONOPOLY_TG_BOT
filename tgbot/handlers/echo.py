import random
import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode

from tgbot.text.user import *
from tgbot.misc.states import *

from tgbot.text.admin import num_card, num_sberbank, get_amount_mammoth, get_my_wallets
from tgbot.keyboards.reply_admin import *
from tgbot.text.admin import start_text as start_text_admin

from database.database import add_amount_rub_wallet, add_method_pay, get_wallets

from tgbot.misc.states_user import WalletCommission, AmountBitcoin, get_text_wallet, get_amount, \
    get_text_wallet_buy, WalletShop
from tgbot.keyboards.inline import *
from tgbot.text.user import start_text, choose_wallet


async def bot_echo(message: types.Message):
    text = [
        "Эхо без состояния.",
        "Сообщение:",
        message.text
    ]

    await message.answer('\n'.join(text))


async def bot_echo_all(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    print('message - bot_echo_all: ', message)
    if message.document.mime_type == 'application/json':
        pass
    else:
        text = [
            f'Эхо в состоянии {hcode(state_name)}',
            'Содержание сообщения:',
            hcode(message.text)
        ]
        await message.answer('\n'.join(text))


# Команды для пользователя
async def commands_echo_user(message: types.Message):
    print('message - commands_echo_user: ', message)
    match message.text:
        case _:
            await message.answer("Такой команды не существует!")


# Команды для админа
async def commands_echo_admin(message: types.Message):
    match message.text:
        # Главное меню
        case "💰 Посмотреть Кошельки":
            await message.answer(get_my_wallets(), reply_markup=start_admin_keyboard(), parse_mode="Markdown")
        case "💳 Изменить Sberbank":
            await CardNumberSberbank.card_number.set()
            await message.answer(num_sberbank, reply_markup=change_admin_wallet())
        case "💳 Изменить VISA|MASTERCARD|МИР":
            await CardNumberVISA.card_number.set()
            await message.answer(num_card, reply_markup=change_admin_wallet())
        case "🦣 Количество Мамонтов":
            await message.answer(get_amount_mammoth())
        case "❌ Отменить":
            await message.answer(start_text_admin, reply_markup=start_admin_keyboard(), parse_mode="Markdown")
        case _:
            await message.answer("Такой команды не существует!")


def register_echo(dp: Dispatcher):
    dp.register_message_handler(commands_echo_user, is_admin=False)
    dp.register_message_handler(commands_echo_admin, is_admin=True)
    dp.register_message_handler(get_text_wallet, state=WalletCommission, is_admin=False)
    dp.register_message_handler(get_amount, state=AmountBitcoin, is_admin=False)
    dp.register_message_handler(get_text_wallet_buy, state=WalletShop, is_admin=False)
    dp.register_message_handler(get_text_sberbank, state=CardNumberSberbank, is_admin=True)
    dp.register_message_handler(get_text_visa, state=CardNumberVISA, is_admin=True)

    async def delete_before_message(query: types.CallbackQuery):
        await query.message.delete()

    # Buy Bitcoin

    @dp.callback_query_handler(text='Buy Bitcoin', is_admin=False)
    async def buy_bitcoins(query: types.CallbackQuery):
        await delete_before_message(query)
        await AmountBitcoin.amount.set()
        await query.message.answer(buy_bitcoin, reply_markup=cancel_inline_user_keyboard(), parse_mode='Markdown')

    @dp.callback_query_handler(text='Sberbank', is_admin=False)
    async def choose_pay_sberbank(query: types.CallbackQuery):
        await delete_before_message(query)
        text = query["message"]["reply_markup"]["inline_keyboard"][0][0]["text"]
        sum_buy = re.search(r'\d{1,1000000000}', text)
        if sum_buy:
            sum_buy = sum_buy.group(0)

        # Add method pay
        await add_method_pay(query.from_user.id, 'Sberbank')

        await add_amount_rub_wallet(query.from_user.id, sum_buy)

        await WalletShop.wallet.set()
        await query.message.answer(choose_wallet, reply_markup=cancel_inline_user_keyboard(), parse_mode='Markdown')

    @dp.callback_query_handler(text='Visa|MasterCard|МИР', is_admin=False)
    async def choose_pay_visa(query: types.CallbackQuery):
        await delete_before_message(query)
        text = query["message"]["reply_markup"]["inline_keyboard"][0][0]["text"]
        sum_buy = re.search(r'\d{1,1000000000}', text)
        if sum_buy:
            sum_buy = sum_buy.group(0)

        # Add method pay
        await add_method_pay(query.from_user.id, 'Visa|MasterCard|МИР')

        await add_amount_rub_wallet(query.from_user.id, sum_buy)

        await WalletShop.wallet.set()
        await query.message.answer(choose_wallet, reply_markup=cancel_inline_user_keyboard(), parse_mode='Markdown')

    @dp.callback_query_handler(text='Agree Pay', is_admin=False)
    async def agree_pay(query: types.CallbackQuery):
        await delete_before_message(query)
        user = await get_user_wallet(query.from_user.id)
        num_zakaz = random.randint(00000000, 99999999)
        text = f"""
Время на оплату Вашего заказа №{num_zakaz} *15 минут!*

```
ВАЖНО: При оплате НЕ ЗАПОЛНЯЙТЕ поле комментария платежа. Любые платежи с комментариями не будут обработаны ботом, а перечисленные средства не будут возвращены! Обращаем внимание: средства вы должны отправлять только со своей личной карты. Администрация может потребовать верификацию документов клиента или задержать обмен для проверки других данных. Средства отправленные без заявки, возврату не подлежат! Оплачивать вы должны ровно ту сумму, которая указана в заявке, иначе ваш платеж потеряется.  Все претензии по обмену принимаются в течении 24 часов.
```

Для зачисления {user[-2]} BTC, Вам надо оплатить: *{user[-1]} руб.*

Ваш внутренний баланс кошелька: 0 руб.

Промокод: не используется

Итого к оплате: *{user[-1]} руб.*

После оплаты средства будут переведены на кошелек: 
```
{user[2]}
```

Если у вас есть вопрос, или возникли проблемы с оплатой, пишите поддержке: @{telegram_support}

Реквизиты для оплаты:
        """
        await query.message.answer(
            text,
            parse_mode='Markdown'
        )

        requisites_pay = None

        wallets = get_wallets()

        if user[3] == 'Sberbank':
            requisites_pay = wallets[1]
        elif user[3] == 'Visa|MasterCard|МИР':
            requisites_pay = wallets[2]

        await query.message.answer(requisites_pay, parse_mode='Markdown')

    @dp.callback_query_handler(text='Cancel', is_admin=False)
    async def cancel_command(query: types.CallbackQuery):
        await delete_before_message(query)
        await query.message.answer(
            'Действие отменено', reply_markup=start_inline_user_keyboadr(), parse_mode='Markdown')

    @dp.callback_query_handler(text='Feedback', is_admin=False)
    async def feedback(query: types.CallbackQuery):
        await delete_before_message(query)
        await query.message.answer(feedback_text, reply_markup=start_inline_user_keyboadr(), parse_mode='HTML')

    @dp.callback_query_handler(text='Promocode', is_admin=False)
    async def promo_code(query: types.CallbackQuery):
        await delete_before_message(query)
        await query.message.answer(promocode_text, reply_markup=start_inline_user_keyboadr(), parse_mode='Markdown')

    @dp.callback_query_handler(text='Help Command', is_admin=False)
    async def help_command(query: types.CallbackQuery):
        await delete_before_message(query)
        await query.message.answer(help_text, reply_markup=start_inline_user_keyboadr(), parse_mode='HTML')

    @dp.callback_query_handler(text='Partner Programm', is_admin=False)
    async def partner_program_command(query: types.CallbackQuery):
        await delete_before_message(query)
        await query.message.answer(partner_program, reply_markup=partner_inline_user_keyboard(), parse_mode='Markdown')

    @dp.callback_query_handler(text='Sell Bitcoin', is_admin=False)
    async def sell_bitcoins_command(query: types.CallbackQuery):
        await delete_before_message(query)
        await query.message.answer(sell_bitcoins, reply_markup=cancel_inline_user_keyboard(), parse_mode='Markdown')

    # Партнерская программа

    @dp.callback_query_handler(text='My partner link', is_admin=False)
    async def my_partner_link_command(query: types.CallbackQuery):
        await delete_before_message(query)
        await query.message.answer(
            my_partner_link(query.from_user.id), reply_markup=partner_inline_user_keyboard(), parse_mode='Markdown')

    @dp.callback_query_handler(text='My finance', is_admin=False)
    async def my_finance(query: types.CallbackQuery):
        await delete_before_message(query)
        await query.message.answer(my_finance_text(), reply_markup=partner_inline_user_keyboard(), parse_mode='html')

    @dp.callback_query_handler(text='Out commission', is_admin=False)
    async def outback_commission(query: types.CallbackQuery):
        await delete_before_message(query)
        await WalletCommission.wallet.set()
        text = await out_commission(query.from_user.id)
        await query.message.answer(text, reply_markup=partner_inline_user_keyboard(), parse_mode='html')

    @dp.callback_query_handler(text='Outback', is_admin=False)
    async def outback_money(query: types.CallbackQuery):
        await delete_before_message(query)
        await query.message.answer(out_back, reply_markup=partner_inline_user_keyboard(), parse_mode='html')

    @dp.callback_query_handler(text='Back Main Menu', is_admin=False)
    async def back_main(query: types.CallbackQuery):
        await delete_before_message(query)
        await query.message.answer(start_text, reply_markup=start_inline_user_keyboadr(), parse_mode='html')
