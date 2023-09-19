from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from DBController import DBController


class FSMLogin(StatesGroup):
    """Класс состояний комманды регистрации преподавателей"""
    start = State()
    login = State()


'''Клавиатура регистрации'''
login_markup = InlineKeyboardMarkup(row_width=1)
user_btn = InlineKeyboardButton(text="Войти как преподаватель", callback_data='Users')
admin_btn = InlineKeyboardButton(text="Войти как администратор", callback_data='Admins')
login_markup.add(user_btn, admin_btn)


async def start(message: types.Message) -> None:
    await FSMLogin.start.set()
    await message.answer(text='Выберете тип входа\nПри ошибке введите "отмена"', reply_markup=login_markup)
    await message.delete()


async def cancel(message: types.Message, state: FSMContext) -> None:
    cur_state = await state.get_state()
    if cur_state is None:
        return
    await state.finish()
    await message.answer("Перевожу на начало регистрации")
    await FSMLogin.start.set()
    await message.answer(text='Выберете тип входа\nПри ошибке введите "отмена', reply_markup=login_markup)


async def login_start(callback_data: types.CallbackQuery, state: FSMContext) -> None:
    """Функция перевода на ожидание ответа от пользователя для входа"""
    async with state.proxy() as data:
        data['msg'] = callback_data.data
    await callback_data.message.answer('Введите логин и пароль через пробел')
    await FSMLogin.next()


async def login_end(message: types.Message, state: FSMContext) -> None:
    """Функция получения логина и пароля от пользователя"""
    newUser = {"login": (message.text.split(' '))[0], "password": (message.text.split(' '))[1]}
    async with state.proxy() as data:
        users = DBController().getNoneAuthUsers() if data['msg'] == 'Users' else DBController().getAdmins()
        newUser['Type'] = data['msg']
    status = 0
    for user in users:
        if newUser["login"] == user["login"] and newUser["password"] == user["password"]:
            status = 1
            newUser['chat_id'] = message.chat.id
            newUser['id'] = user['id']
            newUser['auth'] = 1
            DBController().setChatID(newUser)
            DBController().setAuth(newUser)
            await message.answer(f'Вы вошли как {user["username"]}')
    if not status:
        await message.answer('Неправильно введён логин или пароль, попробуйте снова')
        return
    await state.finish()


async def stop(message: types.Message):
    chatID = message.chat.id
    user = DBController().getEntryByID(chatID)
    user['auth'] = 0
    user['id'] = None
    DBController().setAuth(user)
    DBController().setID(user)
    await message.answer(
        'Вы успешно прервали работу бота и были отключены от рассылки\nДля возобнавления работы введите /start')
    await message.delete()


def Registration_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state=None)
    dp.register_message_handler(cancel, state="start", commands="отмена")
    dp.register_message_handler(cancel, Text(equals="отмена", ignore_case=True), state="start")
    dp.register_message_handler(cancel, state="login", commands="отмена")
    dp.register_message_handler(cancel, Text(equals="отмена", ignore_case=True), state="login")
    dp.register_callback_query_handler(login_start, text=['Users', 'Admins'], state=FSMLogin.start)
    dp.register_message_handler(login_end, state=FSMLogin.login)
    dp.register_message_handler(stop, commands=['stop'])
