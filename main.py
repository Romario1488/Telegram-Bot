# -*- coding: utf-8 -*-
import logging
from os import stat
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sql_queries import pull_stat, add_user_to_db, create_item, change_user_to_admin, pull_items, get_users_number, \
    pull_item_info, del_item, get_clicks, update_clicks, change_users_lang, change_admin_pass
from keyboards import *
from config import *

from aiogram.dispatcher import FSMContext

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup

API_TOKEN = TOKEN
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    u_id = message.from_user.id
    result = add_user_to_db(u_id)
    if not result:
        await message.answer("Добро пожаловать в наш магазин!", reply_markup=markup_main(u_id))
    else:
        await message.answer(f'Рады снова вас видеть, {message.from_user.first_name}!', reply_markup=markup_main(u_id))


class ChangeAdminPass(StatesGroup):
    waiting_for_password = State()
    waiting_for_password_apply = State()
    new_password = []


@dp.message_handler(state=ChangeAdminPass.waiting_for_password, content_types=types.ContentTypes.TEXT)
async def add_item_step_1(message: types.Message, state: FSMContext):
    await message.answer(
        f'Новый пароль для администраторов: {message.text}\n❗️ Все остальные пользователи с правами "Администратор" '
        f'будут разлогинены ❗️\nВы точно хотите сменить пароль для всех пользователей с правами '
        f'"Администратор"?\nНапишите: Да/Нет')
    ChangeAdminPass.new_password.append(message.text)
    await ChangeAdminPass.waiting_for_password_apply.set()


@dp.message_handler(state=ChangeAdminPass.waiting_for_password_apply, content_types=types.ContentTypes.TEXT)
async def add_item_step_1(message: types.Message, state: FSMContext):
    u_id = message.from_user.id
    if message.text == 'Да':
        change_admin_pass(ChangeAdminPass.new_password[0], u_id)
        await message.answer('Пароль успешно изменен!', reply_markup=markup_main(u_id))
        await state.finish()
    elif message.text == 'Нет':
        await message.answer('Отмена смены пароля.', reply_markup=markup_main(u_id))
        await state.finish()
    else:
        await message.answer('Напишите: Да/Нет', reply_markup=markup_main(u_id))
        await ChangeAdminPass.waiting_for_password_apply.set()


class RegisterAdmin(StatesGroup):
    waiting_for_password = State()


@dp.message_handler(state=RegisterAdmin.waiting_for_password, content_types=types.ContentTypes.TEXT)
async def add_item_step_1(message: types.Message, state: FSMContext):
    if message.text == 'test':
        u_id = message.from_user.id
        change_user_to_admin(u_id)
        await message.answer('Верный код доступа\nCтатус изменен на: Администратор', reply_markup=markup_main(u_id))
        await state.finish()
    else:
        await message.answer('Не верный код доступа\nВведите код доступа:')
        await RegisterAdmin.waiting_for_password.set()


class DeleteItemSteps(StatesGroup):
    """Delete item from database"""
    waiting_for_item = State()
    waiting_for_apply_delete = State()
    item_info = []


@dp.message_handler(state=DeleteItemSteps.waiting_for_item, content_types=types.ContentTypes.TEXT)
async def add_item_step_1(message: types.Message, state: FSMContext):
    DeleteItemSteps.item_info = []
    DeleteItemSteps.item_info.append(message.text)
    u_id = message.from_user.id
    if message.text == 'Отменить удаление':
        await message.answer(f'Отмена удаления', reply_markup=markup_main(u_id))
        await state.finish()
    else:
        try:
            result = pull_item_info(message.text)
        except Exception as E:
            await message.answer('Предмет не найден!')
            await DeleteItemSteps.waiting_for_item.set()
        if not result:
            await message.answer('Предмет не найден!')
            await DeleteItemSteps.waiting_for_item.set()
        else:
            await message.answer(f'Удаление предмета\nВы хотите удалить предмет: {result[0]}?',
                                 reply_markup=markup_delete_item)
            await DeleteItemSteps.waiting_for_apply_delete.set()


@dp.message_handler(state=DeleteItemSteps.waiting_for_apply_delete, content_types=types.ContentTypes.TEXT)
async def add_item_step_1(message: types.Message, state: FSMContext):
    u_id = message.from_user.id
    if message.text == 'Удалить':
        try:
            del_item(DeleteItemSteps.item_info[0])
        except Exception as E:
            message.answer('Что-то пошло не так.')
        await message.answer(f'Удаление предмета\nПредмет успешно удален!', reply_markup=markup_main(u_id))
        pull_items()
        await state.finish()
    else:
        await message.answer(f'Отмена удаления', reply_markup=markup_main(u_id))
        await state.finish()


class AddItemSteps(StatesGroup):
    """Add item to database"""
    waiting_for_item_name = State()
    waiting_for_item_price = State()
    waiting_for_item_image = State()
    waiting_for_item_description = State()
    waiting_for_item_flavors = State()
    waiting_for_apply_attrs = State()
    item_info = []


@dp.message_handler(state=AddItemSteps.waiting_for_item_name, content_types=types.ContentTypes.TEXT)
async def add_item_step_1(message: types.Message, state: FSMContext):
    u_id = message.from_user.id
    if message.text == 'Отменить добавление предмета':
        await message.answer('Отмена добавления', reply_markup=markup_main(u_id))
        await state.finish()
    else:
        await message.answer('Добавление нового товара\nУкажите цену: ')

        AddItemSteps.item_info = []
        AddItemSteps.item_info.append(message.text)
        await AddItemSteps.waiting_for_item_price.set()


@dp.message_handler(state=AddItemSteps.waiting_for_item_price, content_types=types.ContentTypes.TEXT)
async def add_item_step_2(message: types.Message, state: FSMContext):
    u_id = message.from_user.id
    if message.text == 'Отменить добавление предмета':
        await message.answer('Отмена добавления', reply_markup=markup_main(u_id))
        await state.finish()
    else:
        if message.text.isdigit():
            await message.answer('Добавление нового товара\nОтправьте фотографию предмета: ')
            AddItemSteps.item_info.append(message.text)
            await AddItemSteps.waiting_for_item_image.set()
        else:
            await message.answer('Цена должна быть указана в цифрах:  ')
            await AddItemSteps.waiting_for_item_price.set()


@dp.message_handler(state=AddItemSteps.waiting_for_item_image, content_types=['photo'])
async def add_item_step_3(message: types.Message, state: FSMContext):
    u_id = message.from_user.id
    if message.text == 'Отменить добавление предмета':
        await message.answer('Отмена добавления', reply_markup=markup_main(u_id))
        await state.finish()
    else:
        await message.answer('Добавление нового товара\nУкажите описание: ')
        await message.photo[-1].download(f'images/{AddItemSteps.item_info[0]}.jpg')
        await AddItemSteps.waiting_for_item_description.set()


@dp.message_handler(state=AddItemSteps.waiting_for_item_description, content_types=types.ContentTypes.TEXT)
async def add_item_step_4(message: types.Message, state: FSMContext):
    u_id = message.from_user.id
    if message.text == 'Отменить добавление предмета':
        await message.answer('Отмена добавления', reply_markup=markup_main(u_id))
        await state.finish()
    else:
        AddItemSteps.item_info.append(message.text)
        await message.answer(f'Добавление нового товара\nУкажите доступные опции:  ')
        await AddItemSteps.waiting_for_item_flavors.set()


@dp.message_handler(state=AddItemSteps.waiting_for_item_flavors, content_types=types.ContentTypes.TEXT)
async def add_item_step_4(message: types.Message, state: FSMContext):
    u_id = message.from_user.id
    if message.text == 'Отменить добавление предмета':
        await message.answer('Отмена добавления', reply_markup=markup_main(u_id))
        await state.finish()
    else:
        AddItemSteps.item_info.append(message.text)
        await message.answer(
            f'Добавление нового товара\nПроверка данных:\n\nНазвание: {AddItemSteps.item_info[0]}\nЦена: {AddItemSteps.item_info[1]}\nОписание: {AddItemSteps.item_info[2]}\nДоступные вкусы: {AddItemSteps.item_info[3]}',
            reply_markup=markup_apply_item)
        await AddItemSteps.waiting_for_apply_attrs.set()


@dp.message_handler(state=AddItemSteps.waiting_for_apply_attrs, content_types=types.ContentTypes.TEXT)
async def add_item_step_4(message: types.Message, state: FSMContext):
    u_id = message.from_user.id
    if message.text == 'Отменить добавление предмета':
        await message.answer('Отмена добавления', reply_markup=markup_main(u_id))
        await state.finish()
    else:
        if message.text == 'Добавить предмет':
            create_item(AddItemSteps.item_info[0], AddItemSteps.item_info[1], f'images/{AddItemSteps.item_info[0]}.jpg',
                        AddItemSteps.item_info[2], AddItemSteps.item_info[3], 0)
            await message.answer(f'Предмет {AddItemSteps.item_info[0]} успешно добавлен!',
                                 reply_markup=markup_main(u_id))
            await state.finish()
        elif message.text == 'Изменить данные':
            await message.answer('Добавление нового товара\nУкажите название: ', reply_markup=markup_stop_item)
            await AddItemSteps.waiting_for_item_name.set()


@dp.message_handler()
async def echo(message: types.Message):
    uid = message.from_user.id
    if message.text == '❓ FAQ':
        if pull_stat(uid)[3] == 'English':
            await message.answer(
                f'Hello, {message.from_user.first_name}!\nInformation',
                reply_markup=markup_main(uid))
        else:
            await message.answer(
                f'Здравствуйте, {message.from_user.first_name}!\nИнформация',
                reply_markup=markup_main(uid))

    elif message.text == 'Добавить новый предмет':
        is_admin = pull_stat(uid)
        users = get_users_number()
        if is_admin[1] == True:
            await message.answer('Добавление нового товара\nУкажите название: ', reply_markup=markup_stop_item)
            await AddItemSteps.waiting_for_item_name.set()
        else:
            await message.answer('Недостаточно прав!')

    elif message.text == '📣 Связаться с нами':
        await message.answer(f'По вопросам обращаться: @test')

    elif message.text == '📣 Contact us':
        await message.answer(f'In case of questions: @test')

    elif message.text == 'RegAdmin':
        is_admin = pull_stat(uid)
        if is_admin[1] == True:
            await message.answer('Вы уже являетесь администратором')
        else:
            await message.answer('Регистрация администратора\nВведите код доступа:', reply_markup=markup_main(uid))
            await RegisterAdmin.waiting_for_password.set()

    elif message.text == '🗂 Каталог':
        await message.answer('Выберите интересующий предмет: ', reply_markup=get_items_list())

    elif message.text == '🗂 Catalog':
        await message.answer('Choose an item: ', reply_markup=get_items_list())

    elif message.text.lower() == 'cменить пароль':
        if uid == MAIN_ADMIN_ID:
            await ChangeAdminPass.waiting_for_password.set()
            await message.answer('Смена пароля\nУкажите новый пароль:', reply_markup=markup_main(uid))
        else:
            await message.answer('Недостаточно прав!')

    elif message.text == 'Статистика':
        is_admin = pull_stat(uid)
        users = get_users_number()
        top5 = get_clicks()
        top5_l = []
        for i in top5:
            top5_l.append(str(i[1]) + " - " + str(i[0]))
        try:
            if is_admin[1] == True:
                await message.answer(
                    f'Статистика\n\nКоличество пользователей: {users[0]}\nКоличество администраторов: {users[1]}\n\nТоп-5 товаров:\n{top5_l[0]}\n{top5_l[1]}\n{top5_l[2]}\n{top5_l[3]}\n{top5_l[4]}',
                    reply_markup=markup_main(uid))
            else:
                await message.answer('Недостаточно прав!')
        except Exception as E:
            await message.answer(
                'Недостаточно товаров в каталоге!\nДля отображения статистики, в каталоге должно быть минимум 5 предметов')

    elif message.text == 'Удалить предмет':
        is_admin = pull_stat(uid)
        users = get_users_number()
        if is_admin[1] == True:
            await message.answer(f'Удаление предмета\nНапишите название предмета:', reply_markup=markup_cancel_delete)
            await DeleteItemSteps.waiting_for_item.set()
        else:
            await message.answer('Недостаточно прав!')

    elif message.text == '🇷🇺 Язык 🇺🇸':
        await message.answer('Смена языка\nВыберите язык:', reply_markup=markup_change_lang)

    elif message.text == '🇷🇺 Language 🇺🇸':
        await message.answer('Choose language:', reply_markup=markup_change_lang)

    elif message.text == "English 🇺🇸":
        change_users_lang('English', uid)
        await message.answer('Switched to English', reply_markup=markup_main(uid))

    elif message.text == "Русский 🇷🇺":
        change_users_lang('Russian', uid)
        await message.answer('Переключение на русский', reply_markup=markup_main(uid))


@dp.callback_query_handler(lambda c: c.data)
async def process_callback(call: types.CallbackQuery):
    update_clicks(call.data)
    item_info = pull_item_info(call.data)
    image = open(f'{item_info[2]}', 'rb')
    await bot.send_photo(call.from_user.id, photo=image,
                         caption=f'{item_info[0]}\n\n{item_info[3]}\n\nДоступные опции: {item_info[5]}\n\nЦена: {item_info[1]} руб.',
                         reply_markup=markup_main(call.from_user.id))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
