import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date

from helpers import apology, login_required

#configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached (credit cs50staff)
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies) (credit cs50staff)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///tracker.db")

# Set some constants
incubation_time = 14

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    #clear current session
    session.clear()

    if request.method == "GET":
        return render_template("login.html")
    #else people post their login
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        #check if form is filled in
        if not username:
            return apology("Please provide a username")
        elif not password:
            return apology("Please provide a password")

        #get the users documentation
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                    username = username)

        #check if username exists
        if len(rows) != 1:
            return apology("Username does not exist")

        #check if the pw matches the hashed pw thats in the database
        elif not check_password_hash(rows[0]["pw_hash"], request.form.get("password")):
            return apology("Incorrect password")

        #safe the user session
        session["user_id"] = rows[0]["user_id"]
        flash("Succesfully logged in")
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

        #if not GET its post
    else:
        """get the form info and save it"""
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # if the fields are blank give error
        if not username:
            return apology("You did not type a valid username")
        elif not password:
            return apology("Please try to guess your password")
        #if passwords dont match give error
        elif password != confirmation:
            return apology("Your passwords don't match")

        #hash the password
        pw_hash = generate_password_hash(request.form.get("password"))

        dbname = db.execute("INSERT INTO users (username, pw_hash) VALUES (:username, :hash)",
                            username = username, hash = pw_hash)
        # if name taken, apology
        if not dbname:
            return apology("name already taken")

        session_id = db.execute("SELECT user_id FROM users WHERE username = :username",
                            username = username)[0]["user_id"]
        session["user_id"] = session_id
    flash("Account created succesfully!")

    return redirect("/")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        user_id = session["user_id"]
        contact = request.form.get("contact").lower()
        date = request.form.get("date")
        location = request.form.get("location")
        memo = request.form.get("memo")

        if not contact:
            return apology("You didn't type a contact")
        if not date:
            return apology("You didn't specify a date")

        db.execute("INSERT INTO history (user_id, contact, date, location, memo) VALUES (:id, :contact, :date, :location, :memo)",
                            id = user_id, contact = contact, date = date, location = location, memo = memo)
        flash("Contact added!")

    return redirect("/")

@app.route("/history")
@login_required
def history():

    rows = db.execute("SELECT * FROM history WHERE user_id = :user_id ORDER BY date",
                user_id = session["user_id"])
    return render_template("history.html", rows = rows)

@app.route("/check", methods=["GET", "POST"])
@login_required
def check():
    #get the date of the test and name of positive tested person
    rows = db.execute("SELECT DISTINCT * FROM history WHERE user_id = :user_id",
                    user_id = session["user_id"])
    if request.method == "GET":
        rows_pos = db.execute("SELECT * FROM positive WHERE user_id= :user_id AND positive =:positive",
                    user_id = session["user_id"], positive = True)

        #go over each positive test and see if there is a risk of being infected
        for row in rows_pos:
            test_pos = row["testdate"]
            contact_pos = row["name"]
            # boolean to check if we encountered a date where the person was infectious
            non_infectious = True

            #grab each date of meeting this person(can be multiple) by the user
            rows_his = db.execute("SELECT date FROM history WHERE user_id = :user_id AND contact = :contact",
                    user_id = session["user_id"], contact = contact_pos)

            #for each meeting date see if its within the incubation period (defined on top of the program) in which case during the meeting the contact could have been infectious
            for dates in rows_his:

                #compare the days between the 2 sql dates(function days_between defined at the bottom)
                delta_date = days_between(test_pos, dates["date"])

                #incubation_time is declared at the top of the program
                #if the meeting was within the incubationtime before the test the person might have been infectious
                #break is for people with multiple meetings otherwise the flash function goes crazy
                if delta_date < incubation_time:
                    non_infectious = False
                    break

                #if non_infectious is still true no dangerous meeting has been detected
            if non_infectious == True:
                db.execute("UPDATE positive SET positive = :false WHERE user_id = :user_id AND name = :name",
                                    false = False, user_id = session["user_id"], name = contact_pos)
                flash(contact_pos+" has likely been noninfectious during the meeting, however take precautions and consider getting tested")

        #update rows_pos for any possible changes
        rows_pos = db.execute("SELECT * FROM positive WHERE user_id= :user_id AND positive =:positive",
                    user_id = session["user_id"], positive = True)
        return render_template("check.html", rows = rows, rows_pos = rows_pos)

    if request.method == "POST":
        contact_pos = request.form.get("contact_pos")
        testdate = request.form.get("date")
        if not testdate:
            return apology("You need to provide a testdate")

        #add the positive test into the database
        db.execute("INSERT INTO positive (name, testdate, positive, user_id) VALUES (:name, :testdate, :positive, :user_id)",
                    name = contact_pos, testdate = testdate, positive = True, user_id = session["user_id"])
        return redirect("/check")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

#calculating the difference between 2 dates, credits to Fred Foo on Stack Overflow (https://stackoverflow.com/questions/8419564/difference-between-two-dates-in-python)
def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)