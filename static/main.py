from flask import Flask, render_template, request, redirect, session
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
import dbHandler
import secrets

# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = secrets.token_hex(64)

# Set secret key for CSRF protection
app.config['SECRET_KEY'] = secrets.token_hex(64)
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

# Initialize CSRF protection
csrf = CSRFProtect(app)

@app.route("/signup.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def signup():
    """if request.method == "GET" and request.args.get("id"):
        url = get_url_from_id(int(request.args.get("id", 0)))
        if url:
            return redirect(url, code=302)"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        if dbHandler.insertUser(username, password, email):
            return render_template("/home.html")
        else:
            return render_template("/signup.html", error="300")
    else:
        return render_template("/signup.html")

@app.route("/home.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def home():
    if request.method == 'POST':
        # if it has recieved input
        session.pop('username', None)
        return redirect('/login.html', code=302)
    else:
        return render_template('/home.html')

@app.route("/kitchen.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def kitchen():
    return render_template("/kitchen.html", content = dbHandler.retPizzas(10)) # change based on viewing size

@app.route('/payment.html', methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def payment():
    
    return render_template('/payment.html')

@app.route('/order_success.html', methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def order_success():
    return render_template('/order_success.html', content=dbHandler.retrieveOrder(uid))

@app.route('/login.html', methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def login():
    if request.method == 'POST':
        det = [request.form['username'], request.form['password'], request.form['user']]
        if det[2] == 'c' and dbHandler.retrieveUsers(det[0], det[1]):
            session['id'] = dbHandler.retrieveUsers(det[0], det[1])
            return redirect('/home.html', code=302)
        elif det[2] == 'd' and dbHandler.retrieveUsers(det[0], det[1]):
            session['id'] = dbHandler.retrieveUsers(det[0], det[1])
            return redirect('/driver.html', code=302)
        else:
            return redirect('/error.html', code=302)
    else:
        return render_template('/login.html')

@a
def logout():


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=3000)