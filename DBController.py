import sqlite3 as sq3


class DBController:
    def __init__(self):

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        # self.text = "1"
        self.db = sq3.connect("ScheduleBotDB.db")
        self.db.row_factory = dict_factory
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def getNoneAuthUsers(self) -> list:
        users: list = self.cursor.execute("select * from User where auth=0 and role=2").fetchall()
        return users

    def getAuthUsers(self) -> list:
        users: list = self.cursor.execute("select * from User where auth=1 and role=2").fetchall()
        return users

    def getUser(self, userName: str) -> dict:
        return self.cursor.execute("select id, username from User where username=?", (userName,)).fetchone()

    def getAdmins(self) -> list:
        admins: list = self.cursor.execute("select * from User where role=(select id from Role where name='Admin')").fetchall()
        return admins

    def getEntryByChatID(self, chat_id: str) -> dict:
        user = self.cursor.execute("select * from User where chat_id=?", (chat_id,)).fetchone()
        if user is None:
            user = {}
        return user

    def setAuth(self, user: dict) -> None:
        query = """UPDATE User SET auth = ? WHERE id = ?"""
        self.cursor.execute(query, (user['auth'], user['id']))
        self.db.commit()

    def setChatID(self, user: dict) -> None:
        query = """UPDATE User SET chat_id = ? WHERE id = ?"""
        self.cursor.execute(query, (user['chat_id'], user['id']))
        self.db.commit()

    def getUserTimetable(self, userName: str, date: str = None) -> list:
        return self.cursor.execute('''select "date", "time", "subject", "room", "user" ,
group_concat("group", ";") "group" FROM Schedule
WHERE "user"=(?) AND "date"=(?) GROUP BY "time";''', (userName, date)).fetchall()

    # def checkID(self, user: dict, userID: str) -> None:
    #     user = self.cursor.execute("select * from Users where Login=:Login and Password=:Password", user).fetchall()
    #     print(user)

    def addUser(self, username: str) -> None:
        self.cursor.execute("insert into 'User'('login', 'password', 'role', 'username') values (?,?,?,?)",
                            (username, username, 2, username))
        self.db.commit()

    def getGroup(self, name: str) -> dict:
        return self.cursor.execute("select * from 'Group' where name=?", (name,)).fetchone()

    def addGroup(self, name: str) -> None:
        self.cursor.execute("insert into 'Group'(name) values (?)",
                            (name,))
        self.db.commit()

    def getSubject(self, name: str) -> dict:
        return self.cursor.execute("select * from 'Subject' where name=?", (name,)).fetchone()

    def addSubject(self, name: str):
        self.cursor.execute("insert into 'Subject'(name) values (?)",
                            (name,))
        self.db.commit()

    def getScheduleEntry(self, user: str, group: str, subject: str, time: str, room: int, date: str) -> list:
        user_id: int = self.cursor.execute("select id from 'User' where username=?", (user,)).fetchone()['id']
        group_id: int = self.cursor.execute("select id from 'Group' where name=?", (group,)).fetchone()['id']
        subject_id: int = self.cursor.execute("select id from 'Subject' where name=?", (subject,)).fetchone()['id']
        return self.cursor.execute(
            "select * from Schedule where user= ? and \"group\"= ? and subject= ? and \"time\"=? and room=? and "
            "\"date\"=?",
            (user_id, group_id, subject_id, time, room, date)
        ).fetchall()

    def addScheduleEntry(self, user: str, group: str, subject: str, time: str, room: int, date: str) -> None:
        user_id: int = self.cursor.execute("select id from 'User' where username=?", (user,)).fetchone()['id']
        group_id: int = self.cursor.execute("select id from 'Group' where name=?", (group,)).fetchone()['id']
        subject_id: int = self.cursor.execute("select id from 'Subject' where name=?", (subject,)).fetchone()['id']
        self.cursor.execute("insert into Schedule values (?,?,?,?,?,?)",
                            (user_id, group_id, subject_id, time, room, date))
        self.db.commit()


if __name__ == "__main__":
    from pprint import pprint

    pprint(DBController().getEntryByID("303759429"))
