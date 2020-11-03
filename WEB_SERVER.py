from flask import Flask, redirect, flash, render_template, jsonify, session, url_for, request
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from CLIENT import Client

# ----global variables----
LenText = 3
LenPwd = 1
messages = []
clients = {}
username = ""

# -----creating heed-----
heed = Flask(__name__)
heed.secret_key = "heed"
heed.permanent_session_lifetime = timedelta(minutes=30)

# -----database-----
heed.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///chat.sqlite3'
heed.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
DataBase = SQLAlchemy(heed)


# ----- class to initialize and save in DataBase -----
class Users(DataBase.Model):
    _id = DataBase.Column("id", DataBase.Integer, primary_key=True)
    name = DataBase.Column(DataBase.String(100))
    username = DataBase.Column(DataBase.String(100))
    password = DataBase.Column(DataBase.String(100))
    email = DataBase.Column(DataBase.String(100))

    def __init__(self, name, username, password, email):
        self.name = name
        self.username = username
        self.password = password
        self.email = email


# ------home page------
@heed.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        return redirect(url_for("login"))
    else:
        return render_template("home.html")


# ------login------
@heed.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if "login" in request.form:
            session.permanent = True
            session["username1"] = request.form["username"]

            # -------- finding username in DataBase --------
            found_user = Users.query.filter_by(username=session["username1"]).first()

            if found_user and request.form["password"] == found_user.password:
                flash(f'Login Successful! welcome : {session["username1"]}')
                global username
                username = session["username1"]
                return redirect(url_for("user", user=session["username1"]))
            else:
                session.pop("username1", None)
                flash("wrong username/password  !!")
                return redirect(url_for("login"))

        if "register" in request.form:
            return redirect(url_for("register"))
    else:
        if "username1" in session:
            flash("Already logged in!")
            return redirect(url_for("user", user=session["username1"]))
        else:
            return render_template("login.html")


# ------user------
@heed.route("/<user>", methods=["POST", "GET"])
def user(user):
    if request.method == "POST":

        if "exit" in request.form:
            # -----fix multiple disconnections------
            clients[session["username1"]].disconnect()
            return redirect(url_for("user", user=session["username1"]))
        else:
            return redirect(url_for("user", user=session["username1"]))

    else:
        if "username1" in session and user == session["username1"]:
            return render_template("user.html", user=session["username1"])
        else:
            flash("You are not logged in!!")
            return redirect(url_for("login"))


# ------register------
@heed.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":

        session.permanent = True
        session["name"] = request.form["name"]
        session["username"] = request.form["username"]
        session["email"] = request.form["email"]

        condition = len(session["name"]) > 3 and len(session["username"]) > 3 and len(session["email"]) > 5
        print(condition)
        if (request.form["t_password"] == request.form["password"]) and condition:
            # ----- adding data to DataBase -----
            found_copy = Users.query.filter_by(username=session["username"]).first()
            if found_copy:
                session.pop("username", None)
                flash("username is taken !!")
                return redirect(url_for("register"))
            else:
                DataBase.session.add(Users(session["name"], session["username"], request.form["password"], session["email"]))
                DataBase.session.commit()
            # ----- popping from session ------
            print("done")
            print(session["name"])
            session.clear()

            flash("Registration Successful")
            return redirect(url_for("login"))
        else:
            if condition:
                session.clear()
                flash(f"length should be greater than {LenText}")
            else:
                flash("!!re-enter password!!")
            return redirect(url_for("register"))
    else:
        if "username" in session:
            return render_template("register.html", name=session["name"], username=session["username"],
                                   email=session["email"])
        else:
            return render_template("register.html")


# ------add any quits possible -----
# ------logout------
@heed.route("/logout")
def logout():
    session.clear()
    flash("Logged Out !!")
    return redirect(url_for("home"))


# functions performed on "join chat" button
@heed.route("/join_chat")
def join_chat():
    clients[session["username1"]] = Client(session["username1"])
    return "none"


# getting msg from text box and sending it to server
@heed.route("/send", methods=["GET"])
def send():
    msg = request.args.get("val")
    clients[session["username1"]].send_messages(msg)
    print(msg)
    return "none"


# to get jsonifyed list of messages
@heed.route("/get_messages")
def get_messages():
    global messages
    messages = clients[session["username1"]].get_messages()
    return jsonify({"messages": messages})


if __name__ == "__main__":
    DataBase.create_all()
    heed.run(debug=True)  # running heed


