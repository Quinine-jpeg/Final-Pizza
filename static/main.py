from flask import Flask, render_template, request, redirect, session
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
import dbHandler
import secrets

# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__, template_folder='../templates', static_folder='../static')
#app.secret_key = secrets.token_hex(64)

# Set secret key for CSRF protection
app.config['SECRET_KEY'] = secrets.token_hex(64)
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

# Initialize CSRF protection
csrf = CSRFProtect(app)

def checkLogin(): #add check for if user is logged on page load
    if session.get('id') is None:
        return redirect('login.html')

@app.route("/signup.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        id = dbHandler.insertUser(username, password, email)
        if id or 'test' in email:
            request.method = 'none'
            session['id'] = id
            return render_template("home.html")
        else:
            return render_template("/signup.html", error="that email is already taken, choose another")
    else:
        return render_template("signup.html")

@app.route("/home.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def home():
    if request.method == 'POST':
        # if it has recieved input, log user out
        session.clear()
        return redirect('login.html', code=302)
    else:
        c = checkLogin()
        if c:
            return c
        return render_template('home.html', ordered=int(bool(dbHandler.retrieveOrder(session['id'], 'userid'))))

@app.route("/kitchen.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def kitchen():
    c = checkLogin()
    if c:
        return c
    return render_template("kitchen.html", content = dbHandler.retPizzas(10)) # change based on viewing size

@app.route('/payment.html', methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def payment():
    if request.method == 'POST':
        dbHandler.addCredit(session['id'], int(request.form['money'])) # yes the other stuff on the page is just fudge
        if session.get('order_num') is None:
            return redirect('payment_success.html')
        else:
            return redirect('order_success.html')
    else:
        c = checkLogin()
        if c:
            return c
        return render_template('payment.html')

@app.route('/order_success.html', methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def order_success():
    c = checkLogin()
    if c:
        return c
    pizzas = []
    order_content = dbHandler.retrieveOrder(session['order_num'], 'id')
    for i in order_content:
        pizzas.append(dbHandler.pizzas_by_id(i[2]))

    return render_template('order_success.html', content=[pizzas, order_content[3:5]])

@app.route('/login.html', methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def login():
    if request.method == 'POST':
        det = [request.form['username'], request.form['password']]
        uid = dbHandler.retrieveUsers(det[0], det[1])
        if uid:
            session['id'] = uid
            session['address'] = dbHandler.retDetails(uid)[4]
            if session['address'] == None:
                session['address'] = ''
            return redirect('/home.html', code=302)
        else:
            return render_template('login.html', error='Email or password is incorrect')
    else:
        return render_template('login.html')

@app.route('/order.html', methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def order():
    if request.method == 'POST': #
        form = request.form
        del form['csrf_token'] # don't need it now
        id = dbHandler.addOrder(form, session['id'], session['address'])
        session['order_num'] = id
        return redirect('order_success.html')
    else:#
        c = checkLogin()
        if c:
            return c
        return render_template('order.html', content=(dbHandler.retMenu(), session['address']))
    
@app.route('/', methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def landing():
    if session.get('id'):
        return redirect('home.html')
    else:
        return redirect('login.html')
    
@app.route('/manager.html', methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def manager():
    if request.method == 'POST':
        if request.form['id'] == 'pizza':
            print(f'New pizza added: {request.form['name']}')
            name = request.form['name']
            descrip = request.form['descrip']
            price = request.form['price']
            dbHandler.addPizza(name, descrip, price)
            return render_template('manager.html', content=(dbHandler.allOrders(), f'created pizza: {name}'))
        else:
            num = request.form['order']
            dbHandler.progressOrder(num)
            return render_template('manager.html', content=(dbHandler.allOrders(), f'progressed order number {num}'))
    else:
        return render_template('manager.html', content=(dbHandler.allOrders(), ''))

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=3000)