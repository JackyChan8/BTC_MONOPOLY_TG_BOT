import os

from database.database import get_wallets, get_mammoths

start_text = f'🎉 Добро пожаловать в админку бота {os.environ.get("NAME_SERVICE")}'
num_card = '💳 Введите номер Банковской Карты VISA|MASTERCARD|МИР: '
num_sberbank = '💳 Введите номер Банковской Карты Sberbank: '
num_btc = '₿ Введите номер Bitcoin Кошелька: '
upload_data = 'Добавьте файл с данными формата json'


def get_amount_mammoth():
    # Запрос в Базу данных на количество мамонтов
    mammoths = get_mammoths()
    if mammoths:
        amount_mammoth = len(mammoths)
        mammoths = [f'id: {m[0]} \nUsername: @{m[1]} \nReferral ID: {m[2]}' for m in mammoths]
        mammoths = "\n\n".join(el for el in mammoths)
        return f'''
🦣: {amount_mammoth} мамонтов

Список мамонтов:
{mammoths}
        '''
    else:
        amount_mammoth = 0
        return f'''
        🦣: {amount_mammoth} мамонтов
        '''


def get_my_wallets():
    # Запрос в Базу данных для получения кошельков
    wallets = get_wallets()

    return f"""
Ваши установленные кошельки:

💳 Sberbank: ```{wallets[1]}```
💳 VISA|MasterCard|МИР: ```{wallets[2]}```
    """
