import sqlite3 as sql

order_progress = {

}

def insertUser(username, password, email):
    con = sql.connect("../database/data.db")
    cur = con.cursor()
    cur.execute(f"select * from users where email = '{email}'")
    if cur.fetchall() != []:
        con.close()
        return False
    cur.execute(
        "INSERT INTO users (username, password, email, credit) VALUES (?,?,?,?)",
        (username, password, email, 0)
    )
    con.commit()
    cur.execute("select last_insert_rowid()")
    v = cur.fetchone()
    con.close()
    return v

def retrieveUsers(username, password):
    con = sql.connect("../database/data.db")
    cur = con.cursor()
    cur.execute(f"SELECT id FROM users WHERE email = '{username}' and password = '{password}'")
    id = cur.fetchone()
    con.close()
    if id:
        return id[0]
    
def addOrder(pizza, uid, address=None):
    for i in pizza.keys():
        if pizza[i] == 0:
            del pizza[i]
    
    pizzas = []
    for i in pizza.keys():
        for j in range(pizza[i]):
            pizzas.append(i)

    pizzas = ', '.join(pizzas)

    con = sql.connect('../database/data.db')
    cur = con.cursor()

    if address == None and uid:
        cur.execute(f"select address from users where id = '{uid}'")
        address = cur.fetchone()

    cur.execute(f"insert into orders (userid, pizzas, address, status, price) values (?,?,?,?,?)", (uid, pizzas, address, 'unpaid', sum(pizza.values())))
    con.commit()
    cur.execute("select last_insert_rowid()")
    v = cur.fetchone()[0]
    con.close()
    return v

def retrieveOrder(id):
    con = sql.connect('../database/data.db')
    cur = con.cursor()
    cur.execute(f"select * from orders where id = ?", (id,))
    v = cur.fetchone()
    con.close()
    return v

def retPizzas(num:int):
    "find next [num] pizzas"
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
                pizzas.append(pizzas_by_id(j))
                if len(pizzas) == num:
                    return pizzas, inst
                    # quicker than double breaking

    con.close()
    return pizzas, inst

def retMenu():
    "show user all available pizzas"
    con = sql.connect('../database/data.db')
    cur = con.cursor()
    cur.execute('select name, price, descrip from pizzas order by id')
    v = cur.fetchall()
    con.close()
    return v 

def confOrder(order_num):
    'Confirm that customer has paid for order'
    con = sql.connect('../database/data.db')
    cur = con.cursor()
    cur.execute(f"select userid, price from orders where id = ?", (order_num,))
    r = cur.fetchone()
    uid = r[0]
    price = r[1]
    cur.execute(f"select credit from users where id = ?", (uid,))
    if cur.fetchone()[0] >= price:
        cur.execute(f"update orders set status = 'pending' where id = ?", (order_num,))
        con.close()
        return True
    else:
        con.close()
        return False

def addCredit(uid, amt):
    con = sql.connect('../database/data.db')
    cur = con.cursor()
    cur.execute(f"update users set credit = credit + ? where id = ?", (amt, uid))
    con.commit()
    con.close()

def pizzas_by_id(id):
    con = sql.connect('../database/data.db')
    cur = con.cursor()
    cur.execute(f"select * from pizzas where id = '{id}'")
    v = cur.fetchone()
    con.close()
    return v

def retDetails(id):
    con = sql.connect('../database/data.db')
    cur = con.cursor()
    cur.execute(f"select username, email, password, credit, address from users where id = {id}")
    det = cur.fetchone()
    con.close()
    return det

def progressOrder(num):
    con = sql.connect('../database/data.db')
    cur = con.cursor()
    cur.execute(f'update')

def addPizza(name, descrip, price):
    con = sql.connect('../database/data.db')
    cur = con.cursor()
    cur.execute(f"INSERT INTO pizzas (name, price, descrip) VALUES (?,?,?)", (name, price, descrip))
    con.commit()
    con.close()

def allOrders():
    con = sql.connect('../database/data.db')
    cur = con.cursor()
    cur.execute(f'select id, status from orders')
    ret = cur.fetchall()
    con.close()
    return ret

def ordersByUid(id):
    con = sql.connect('../database/data.db')
    cur = con.cursor()
    cur.execute('select id from orders where userid = ?', (id,))
    