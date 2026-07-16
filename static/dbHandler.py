import sqlite3 as sql
import time
import random

pizza_ids = {
    1: 'cheese',
    2: 'pepperoni'
} # add more as necessary

def insertUser(username, password, email):
    con = sql.connect("../database/data.db")
    cur = con.cursor()
    cur.execute(f"select * from users where email = {email}")
    if cur.fetchall() != None:
        return False
    cur.execute(
        "INSERT INTO users (username,password,email) VALUES (?,?,?)",
        (username, password, email)
    )
    con.commit()
    con.close()
    return True

def retrieveUsers(username, password=None):
    con = sql.connect("../database/data.db")
    cur = con.cursor()
    if password:
        cur.execute(f"SELECT * FROM users WHERE email = '{username}' and password = '{password}'")
        if cur.fetchone() == None:
            con.close()
            return None
        else:
            return cur.fetchone()[0]
    else:
        cur.execute(f"select * from users where email = '{username}'")
        return cur.fetchone()[0]

def addOrder(pizzas, uid='g', address=None):
    pizzas = ' '.join(pizzas)
    con = sql.connect('../database/data.db')
    cur = con.cursor()

    if address == None and uid:
        cur.execute(f"select address from users where id = '{uid}'")
        address = cur.fetchone()

    cur.execute(f"insert into orders (userid, pizzas, address) values ({uid, pizzas, address})")
    cur.execute("select last_insert_rowid()")
    con.close()
    return cur.fetchone()


def retrieveOrder(id, criteria):
    "find what orders fill a criteria"
    con = sql.connect('../database/data.db')
    cur = con.cursor()
    cur.execute(f"select * from orders where {criteria} = {id}")
    con.close()
    return cur.fetchall()

def addPizza(name):
    con = sql.connect('../database/data.db')
    cur = con.cursor()
    cur.execute(f"insert into pizzas (name) values ({name})")
    con.close()

def retPizzas(num:int):
    "find next [num] pizzas"
    print('called function')
    pizzas = []
    inst = {}
    con = sql.connect('../database/data.db')
    cur = con.cursor()
    cur.execute(f"select * from orders where status = 'pending' order by id")
    orders = cur.fetchall()
    for i in orders:
        inst[i[0]] = i[5]
        for j in i[2]:
            if j.isnumeric():
                pizzas.append(pizza_ids[j])
                if len(pizzas) == num:
                    return pizzas, inst
                    # quicker than double breaking

    return pizzas, inst

def retMenu():
    "show user all available pizzas"
    con = sql.connect('../database/data.db')
    cur = con.cursor()
    cur.execute('select * from pizzas order by id')
    con.close()
    return cur.fetchall()

def confOrder():
    'Confirm that customer has paid for order'
