import time
import schedule
from multiprocessing import Process
from aiogram.utils import executor
from init_bot import dp
from Registration import Registration
from Admin import Admin, Check
from Service import ServiceFunctions


class ScheduleMessage:
    @staticmethod
    def try_send():
        while True:
            schedule.run_pending()
            time.sleep(1)

    @staticmethod
    def start_process():
        process = Process(target=ScheduleMessage.try_send, args=())
        process.start()


schedule.every().day.at("18:00").do(ServiceFunctions.sendTimetable)

if __name__ == "__main__":
    Registration.Registration_handlers(dp)
    Admin.Admin_Handlers(dp)
    Check.Check_Handlers(dp)

    ServiceFunctions.Service_handlers(dp)

    ScheduleMessage.start_process()

    executor.start_polling(dp, skip_updates=True)
