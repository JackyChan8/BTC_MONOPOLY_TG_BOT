import os
import requests

from database.database import get_user_wallet, get_amount_price


def get_price(symbol):
    res = requests.get(f'https://api.binance.com/api/v1/ticker/24hr?symbol=BTC{symbol}')

    if res.status_code == 200:
        price = float(res.json()['lastPrice'])
        return price


def get_price_rub(price):
    res = requests.get(f'https://blockchain.info/tobtc?currency=RUB&value={price}')
    if res.status_code == 200:
        return res.text


def to_fixed(numObj, digits=0):
    return f"{numObj:.{digits}}"


name_service = os.environ.get("BOT_NICKNAME")
telegram_support = os.environ.get("TELEGRAM_SUPPORT")
review_chat = os.environ.get("REVIEW_CHAT")
news_channel = os.environ.get("NEWS_CHANNEL")
monopoly_bot = os.environ.get('USERNAME_BOT')

start_text = f"""
✌️ Бот обменник! <a href="https://i.vgy.me/52boQl.png">  </a>

Тут ты можешь обменять свои RUB на BTC

Если ты "новичок" и хочешь получить промокод на скидку? - пиши мне @{telegram_support}

Жми кнопку "👉 Купить Биткоин 👈" или просто введи сумму в RUB или BTC

Пример: 0.001 или 0,001
"""

buy_bitcoin = """
Укажите сумму в BTC:

```
Пример: 0.001 или 0,001 или 5000
```
"""


async def choose_method_pay(id):
    choose_amount = await get_amount_price(id, 'amount_btc')
    if ',' in choose_amount:
        choose_amount = choose_amount.replace(',', '.')
    btc_usd = get_price('USDT')
    if ',' in choose_amount or '.' in choose_amount:
        # Получаем курс BTC/USD
        return f"""
Средний рыночный курс BTC ${round(btc_usd, 2)}
    
Вы получите: *{float(choose_amount):.5f} BTC*
    
Ваш внутренний баланс кошелька: *0 руб.*
    
Для продолжения выберите *Способ 
оплаты*:
    
"Если способов оплаты не видишь, - мониторь, они регулярно появляются! Поддержку не нужно отвлекать по этому вопросу."
    """
    else:
        choose_amount = get_price_rub(choose_amount)
        return f"""
Средний рыночный курс BTC ${round(btc_usd, 2)}

Вы получите: *{float(choose_amount):.5f} BTC*

Ваш внутренний баланс кошелька: *0 руб.*

Для продолжения выберите *Способ 
оплаты*:

"Если способов оплаты не видишь, - мониторь, они регулярно появляются! Поддержку не нужно отвлекать по этому вопросу."
        """


choose_wallet = """
*Скопируйте и отправьте боту свой кошелек BTC*. Бот сохранит его и при следующем обмене предложит в виде *удобной кнопки ниже:*
"""

feedback_text = f"""
<b>Контакты поддержки:</b>

@{telegram_support}

<b>Наш канал с отзывами:</b>

@{review_chat}

<b>Новости нашего обменника, а также промокоды, акции и конкурсы в нашем официальном канале:</b>

@{news_channel}
"""

promocode_text = f"""
Вы не используете промокод в настоящее время.

Напишите боту промокод, чтобы активировать его!

Собирать промокоды на *одном аккаунте* ЗАПРЕЩЕНО!

Если ты "новичок" и хочешь получить промокод на скидку? - пиши мне @{telegram_support}
"""

help_text = f"""
<b>Инструкция как пользоваться ботом:</b>

https://teletype.in/@btcmonopoly/rkonw2aZU

<b>Видеоинструкция:</b>

https://www.youtube.com/watch?v=s4dkqKoxgG8

<b>Не разобрался с ботом? Пиши мне, проведем обмен вручную:</b>

@{telegram_support}

<b>Промокоды, акции, а также всегда свежие новости в нашем канале:</b>

@{news_channel}

<b>Наш канал с отзывами:</b>

@{review_chat}
"""

sell_bitcoins = f"""
Покупаем от 10000 руб. Если хотите продать BTC, пишите @{telegram_support}
"""

partner_program = """
*Условия партнерской программы:*

Рекомендуйте наш сервис, стройте команду и получайте вознаграждение от каждого обмена привлеченных вами клиентов!

Минимальная сумма на вывод: 0.005 BTC

⚠️Внимание! Вывод заработанных средств в Monopoly Casino, невозможен. Заработанные деньги вы можете использовать, как скидку для обмена в BTC Monopoly или же продолжить играть в Monopoly Casino.

Вывод средств по запросу!
"""


def my_partner_link(id):
    return f"""
Ваша ссылка для приглашения партнеров:

https://t.me/{monopoly_bot}?start={id}
    """


def my_finance_text():
    return """
Количество партнеров в моей команде: 0

Активные партнеры: 0

Оплаченых заказов: 0

На балансе: 0 руб.

Минимальная сумма на вывод: 0.005 BTC
"""


async def out_commission(id):
    check_exist = await get_user_wallet(id)
    if check_exist:
        text = f"""
Ранее вы указали данный BTC адрес {check_exist[1]}

Введите ваш BTC кошелек:
        """
    else:
        text = """
У вас еще не указан кошелек для выплат комиссионных.
    
Введите ваш BTC кошелек:
        """
    return text


out_back = """
Пока что у Вас нет партнерских вознаграждений.

Вы сможете запросить вывод средств, если сумма реферальных вознаграждений достигла или превышает 0.005 BTC
"""
# ============================================================
referral_link_text = '❗ Нельзя регистрироваться по собственной реферальной ссылке!'
