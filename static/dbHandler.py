import sqlite3 as sql
import time
import random


def insertUser(username, password, email):
    con = sql.connect("../database/data.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (username,password,email) VALUES (?,?,?)",
        (username, password, email),
    )
    con.commit()
    con.close()


def retrieveUsers(username, password):
    con = sql.connect("../database/data.db")
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

def addOrder(pizzas, uid='g', address=None):
    pizzas = ' '.join(pizzas)
    con = sql.connect('../database/data.db')
    cur = con.cursor()

    if address == None and uid:
        cur.execute(f"select address from users where id = '{uid}'")
        address = cur.fetchone()

    cur.execute(f"insert into orders (userid, pizzas, address) values ({uid, pizzas, address})")
    con.close()

def retrieveOrder(id, criteria):
    con = sql.connect('../database/data.db')
    cur = con.cursor()
    cur.execute(f"select * from orders where {criteria} = {id}")
    con.close()
    return cur.fetchall()

