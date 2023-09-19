from init_bot import bot
from DBController import DBController
from datetime import date, timedelta
from aiogram import types, Dispatcher


async def sendTimetable():
    users: list = DBController().getAuthUsers()

    for user in users:
        userID = DBController().getUser(user["Name"])["ID"]
        timetable: list = DBController().getUserTimetable(user['Name'],
                                                          (date.today() + timedelta(days=1)).strftime('%d.%m.%y'))
        # timetable: list = DBController().getUserTimetable(user['Name'], "06.09.22")

        for entry in timetable:
            await bot.send_message(userID,
                                   f"{entry['Date']}\nГруппы: {entry['Groups']}\nПредмет: {entry['Object']}\nВремя: {entry['Time']}")


async def sendMyTimetable(message: types.Message):
    userID = message.chat.id
    user = DBController().getEntryByID(userID)
    timetable: list = DBController().getUserTimetable(user['Name'],
                                                      (date.today() + timedelta(days=1)).strftime('%d.%m.%y'))

    for entry in timetable:
        await bot.send_message(userID,
                               f"{entry['Date']}\nГруппы: {entry['Groups']}\nПредмет: {entry['Object']}\nВремя: {entry['Time']}")


def Service_handlers(dp: Dispatcher):
    dp.register_message_handler(sendTimetable, commands=['time'])
    dp.register_message_handler(sendMyTimetable, commands=['расписание'])


if __name__ == "__main__":
    sendTimetable()
