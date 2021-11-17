from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from sql_queries import pull_stat, pull_items
from aiogram import types


def markup_main(uid):
    is_admin = pull_stat(uid)
    if pull_stat(uid)[3] == 'English':

        if is_admin[1] == True:

            btn1 = KeyboardButton('🗂 Catalog ')
            btn2 = KeyboardButton('❓ FAQ ')
            btn3 = KeyboardButton('📣 Contact us ')
            btn4 = KeyboardButton('🇷🇺 Language 🇺🇸')
            btn5 = KeyboardButton('Добавить новый предмет')
            btn6 = KeyboardButton('Удалить предмет')
            btn7 = KeyboardButton('Статистика')
            markup_mail_success = ReplyKeyboardMarkup(resize_keyboard=True).add(btn1).add(btn2).add(btn3, btn4).add(
                btn5, btn6).add(btn7)

        else:
            btn1 = KeyboardButton('🗂 Catalog ')
            btn2 = KeyboardButton('❓ FAQ ')
            btn3 = KeyboardButton('📣 Contact us ')
            btn4 = KeyboardButton('🇷🇺 Language 🇺🇸')
            markup_mail_success = ReplyKeyboardMarkup(resize_keyboard=True).add(btn1).add(btn2).add(btn3, btn4)
        return markup_mail_success
    else:

        if is_admin[1] == True:

            btn1 = KeyboardButton('🗂 Каталог ')
            btn2 = KeyboardButton('❓ FAQ ')
            btn3 = KeyboardButton('📣 Связаться с нами ')
            btn4 = KeyboardButton('🇷🇺 Язык 🇺🇸')
            btn5 = KeyboardButton('Добавить новый предмет')
            btn6 = KeyboardButton('Удалить предмет')
            btn7 = KeyboardButton('Статистика')
            markup_mail_success = ReplyKeyboardMarkup(resize_keyboard=True).add(btn1).add(btn2).add(btn3, btn4).add(
                btn5, btn6).add(btn7)

        else:
            btn1 = KeyboardButton('🗂 Каталог ')
            btn2 = KeyboardButton('❓ FAQ ')
            btn3 = KeyboardButton('📣 Связаться с нами ')
            btn4 = KeyboardButton('🇷🇺 Язык 🇺🇸')
            markup_mail_success = ReplyKeyboardMarkup(resize_keyboard=True).add(btn1).add(btn2).add(btn3, btn4)
        return markup_mail_success


def markup_main_eng(uid):
    is_admin = pull_stat(uid)


btn1 = KeyboardButton('Добавить предмет')
btn2 = KeyboardButton('Изменить данные')

markup_apply_item = ReplyKeyboardMarkup(resize_keyboard=True).add(btn1).add(btn2)

btn1 = KeyboardButton('Удалить')
btn2 = KeyboardButton('Отменить удаление')

markup_delete_item = ReplyKeyboardMarkup(resize_keyboard=True).add(btn1).add(btn2)

btn1 = KeyboardButton('Русский 🇷🇺')
btn2 = KeyboardButton('English 🇺🇸')

markup_change_lang = ReplyKeyboardMarkup(resize_keyboard=True).add(btn1).add(btn2)

btn1 = KeyboardButton('Отменить удаление')

markup_cancel_delete = ReplyKeyboardMarkup(resize_keyboard=True).add(btn1)

btn1 = KeyboardButton('Отменить добавление предмета')
markup_stop_item = ReplyKeyboardMarkup(resize_keyboard=True).add(btn1)


def get_items_list():
    all_items = pull_items()
    inline_kb_pay = InlineKeyboardMarkup()
    for i in all_items:
        inline_kb_pay.add(InlineKeyboardButton(i[0], callback_data=i[0]))

    return inline_kb_pay
