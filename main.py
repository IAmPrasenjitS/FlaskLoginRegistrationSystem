from flask import Flask, render_template, redirect, url_for, request, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Required for Database Connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "mydb"

mysql = MySQL(app)

@app.route("/")
def home():
    if "username" in session:
        return render_template("home.html")
    return redirect("/login")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")

@app.route("/loginAction", methods=['POST'])
def loginAction():
    if request.method == "POST":
        username = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM `users` WHERE `email` = %s AND `pass` = %s", (username, password))
        data = cur.fetchone()
        if data:
        # dbUName = "pro.prasenjit@gmail.com"
        # dbPassword = "pro.prasenjit"
        # if request.form['email'] == "pro.prasenjit@gmail.com" and request.form['password'] == "pro.prasenjit":
            session['username'] = username
            return redirect("/")
           #  return "Inside If"
        else:
            return redirect(url_for("login"))

@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route("/action", methods=["POST"])
def action():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `users` (`id`, `name`, `email`, `pass`) VALUES (NULL, %s, %s, %s)", (name, email, password))
    mysql.connection.commit()
    cur.close()
    # return "Data Inserted"
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)