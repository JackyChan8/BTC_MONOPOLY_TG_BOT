import re

from tgbot.text.user import buy_bitcoin, choose_wallet
from tgbot.keyboards.inline import cancel_inline_user_keyboard


async def validate_form(form_field, message):
    match form_field:
        case "card_number":
            if not message.text.isdigit():
                await message.reply(f'Номер карты должен состоять из цифр!', parse_mode='Markdown')
            elif not len(message.text) == 16:
                await message.reply(f'Номер карты должен быть длинной равной 16 символов', parse_mode='Markdown')
            else:
                return True
        case "bitcoin_wallet":
            pattern_btc = r'(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}'
            bitcoin = re.search(pattern_btc, message.text)
            if not bitcoin:
                await message.answer(f'Неправильный формат Bitcoin кошелька!', parse_mode='Markdown')
                await message.answer(choose_wallet, reply_markup=cancel_inline_user_keyboard(), parse_mode='Markdown')
            else:
                return True
        case "amount":
            if message.text.isdigit():
                return True
            else:
                try:
                    if isinstance(float(message.text), float):
                        return True
                except ValueError:
                    if ',' in message.text:
                        text_user = message.text.replace(',', '.')
                        if text_user.isdigit():
                            return True
                        else:
                            try:
                                if isinstance(float(text_user), float):
                                    return True
                            except ValueError:
                                await message.answer('Не верная сумма обмена!')
                                await message.answer(buy_bitcoin, reply_markup=cancel_inline_user_keyboard(),
                                                     parse_mode='Markdown')
                                return False
                    else:
                        await message.answer('Не верная сумма обмена!')
                        await message.answer(buy_bitcoin, reply_markup=cancel_inline_user_keyboard(), parse_mode='Markdown')
                        return False
        case _:
            pass
