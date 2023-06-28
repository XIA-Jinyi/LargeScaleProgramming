import sqlite3
import time
from threading import Lock


db_lock = Lock()


def init(db_path):
    with db_lock:
        with sqlite3.connect(db_path) as db_conn:
            db_conn.execute(
                """
                CREATE TABLE UserTable (
                    email       VARCHAR(64) PRIMARY KEY,
                    username    VARCHAR(32) NOT NULL,
                    pwdhash     CHAR(64)    NOT NULL
                )
                """
            )
            db_conn.execute(
                """
                CREATE TABLE FriendTable (
                    email1 VARCHAR(64),
                    email2 VARCHAR(64),
                    FOREIGN KEY (email1) REFERENCES UserTable(email)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE,
                    FOREIGN KEY (email2) REFERENCES UserTable(email)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE,
                    PRIMARY KEY (email1, email2)
                )
                """
            )
            db_conn.execute(
                """
                CREATE TABLE FriendRequest (
                    inviter         VARCHAR(64),
                    invitee         VARCHAR(64),
                    request_time    FLOAT   NOT NULL,
                    FOREIGN KEY (inviter) REFERENCES UserTable(email)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE,
                    FOREIGN KEY (invitee) REFERENCES UserTable(email)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE,
                    PRIMARY KEY (inviter, invitee)
                )
                """
            )


def find_user(db_path, email) -> str | None:
    with db_lock:
        with sqlite3.connect(db_path) as db_conn:
            cursor = db_conn.execute(
                f"""
                SELECT username FROM UserTable
                WHERE email = \'{email}\'
                """
            )
            all = cursor.fetchall()
    if len(all) == 0:
        return None
    else:
        return all[0][0]


def get_pwdhash(db_path, email) -> str | None:
    with db_lock:
        with sqlite3.connect(db_path) as db_conn:
            cursor = db_conn.execute(
                f"""
                SELECT pwdhash FROM UserTable
                WHERE email = \'{email}\'
                """
            )
            all = cursor.fetchall()
    if len(all) == 0:
        return None
    else:
        return all[0][0]


def register(db_path, email, username, pwdhash):
    with db_lock:
        with sqlite3.connect(db_path) as db_conn:
            db_conn.execute(
                f"""
                INSERT INTO UserTable
                VALUES (\'{email}\', \'{username}\', \'{pwdhash}\')
                """
            )
            db_conn.commit()


def raise_friend_request(db_path, inviter, invitee):
    with db_lock:
        with sqlite3.connect(db_path) as db_conn:
            cursor = db_conn.execute(
                f"""
                SELECT * FROM FriendRequest
                WHERE inviter = \'{inviter}\' AND invitee = \'{invitee}\'
                """
            )
            if len(cursor.fetchall()) == 1:
                return
            db_conn.execute(
                f"""
                INSERT INTO FriendRequest
                VALUES (\'{inviter}\', \'{invitee}\', {time.time()})
                """
            )
            db_conn.commit()


def get_friend_request(db_path, invitee) -> list[tuple[str, str]]:
    with db_lock:
        with sqlite3.connect(db_path) as db_conn:
            cursor = db_conn.execute(
                f"""
                SELECT inviter, username
                FROM FriendRequest
                INNER JOIN UserTable
                ON FriendRequest.inviter = UserTable.email
                WHERE invitee = \'{invitee}\'
                """
            )
            request_list = []
            for line in cursor.fetchall():
                request_list.append((line[0], line[1]))
            db_conn.execute(
                f"""
                DELETE FROM FriendRequest
                WHERE invitee = \'{invitee}\'
                """
            )
            db_conn.commit()
    return request_list


def add_friend(db_path, email1, email2):
    with db_lock:
        with sqlite3.connect(db_path) as db_conn:
            db_conn.execute(
                f"""
                INSERT INTO FriendTable
                VALUES (\'{email1}\', \'{email2}\')
                """
            )
            db_conn.commit()


def get_friend_list(db_path, email) -> list[tuple[str, str]]:
    with db_lock:
        with sqlite3.connect(db_path) as db_conn:
            cursor = db_conn.execute(
                f"""
                SELECT email, username
                FROM UserTable
                INNER JOIN FriendTable
                ON UserTable.email = FriendTable.email1
                WHERE email2 = \'{email}\'
                UNION
                SELECT email, username
                FROM UserTable
                INNER JOIN FriendTable
                ON UserTable.email = FriendTable.email2
                WHERE email1 = \'{email}\'
                """
            )
            friend_list = []
            for line in cursor.fetchall():
                friend_list.append((line[0], line[1]))
    return friend_list


def judge_friend(db_path, email1, email2) -> bool:
    with db_lock:
        with sqlite3.connect(db_path) as db_conn:
            cursor = db_conn.execute(
                f"""
                SELECT * FROM FriendTable
                WHERE email1 = \'{email1}\' AND email2 = \'{email2}\'
                OR email2 = \'{email1}\' AND email1 = \'{email2}\'
                """
            )
            return len(cursor.fetchall()) == 1


def del_friend(db_path, user, friend):
    with db_lock:
        with sqlite3.connect(db_path) as db_conn:
            db_conn.execute(
                f"""
                DELETE FROM FriendTable
                WHERE email1 = \'{user}\' AND email2 = \'{friend}\'
                """
            )
            db_conn.execute(
                f"""
                DELETE FROM FriendTable
                WHERE email2 = \'{user}\' AND email1 = \'{friend}\'
                """
            )
            db_conn.commit()
