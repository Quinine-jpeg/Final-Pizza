import sqlite3 as sql
import time
import random


def insertUser(username, password, email):
    con = sql.connect("../database_files/database.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (username,password,email,uid) VALUES (?,?,?)",
        (username, password, email),
    )
    con.commit()
    con.close()


def retrieveUsers(username, password):
    con = sql.connect("../database_files/database.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM users WHERE username = '{username}' and password = '{password}'")
    if cur.fetchone() == None:
        con.close()
        return False
    else:
        # Plain text log of visitor count as requested by Unsecure PWA management
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w") as file:
            file.write(str(number))
        # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000)
        con.close()
        return True


