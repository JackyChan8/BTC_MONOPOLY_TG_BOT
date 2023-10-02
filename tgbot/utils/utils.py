import json
from aiogram.types import KeyboardButton
from database.database import get_data_shop


def create_button_reply(words, menu, product=None):
    """"""
    if not isinstance(words, dict):
        for _, num in zip(words, range(1, len(words) + 1, 2)):
            if num == len(words) and len(words) % 2 != 0:
                menu.add(KeyboardButton(words[len(words) - 1]))
                break
            elif num > len(words):
                break
            else:
                menu.add(KeyboardButton(words[num - 1]), KeyboardButton(words[num]))
        menu.add(KeyboardButton('❌ Отменить'))
        return menu
    else:
        if product == 'Экстази':
            for i in words:
                weight = words[i]['Вес']
                price = words[i]['Цена']
                menu.add(KeyboardButton(f'{weight}шт ({price} руб)'))
        else:
            for i in words:
                weight = words[i]['Вес']
                price = words[i]['Цена']
                menu.add(KeyboardButton(f'{weight}г ({price} руб)'))
        menu.add(KeyboardButton('❌ Отменить'))
        return menu


def get_cities():
    """Получить все города"""
    result = get_data_shop()
    json_data = json.loads(result[1])[0]
    cities = [data for data in json_data]
    return cities


def get_areas(city):
    """Получить Районы"""
    result = get_data_shop()
    json_data = json.loads(result[1])[0]
    areas = list(json_data[city].keys())
    return areas


def get_products(city, area):
    """Получить продукты"""
    result = get_data_shop()
    json_data = json.loads(result[1])[0]
    products = list(json_data[city][area].keys())
    return products


def get_packaging(city, area, product):
    """Получить цены"""
    result = get_data_shop()
    json_data = json.loads(result[1])[0]
    packaging = [json_data[city][area][product]][0]
    return packaging
