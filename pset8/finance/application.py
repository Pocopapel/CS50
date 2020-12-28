import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():

    #get username (could do through id but then we would have to remake the table)
    username = db.execute("SELECT username FROM users WHERE id = :id",
                    id = session["user_id"])[0]["username"]

    #get the shares the user has, each row is one share
    rows = db.execute("SELECT * FROM shares WHERE username = :username",
                    username = username)

    #get current cash
    cash = db.execute("SELECT cash FROM users WHERE id = :id",
                    id = session["user_id"])[0]["cash"]
    total = cash

    for row in rows:
        #save the info of this share and add name, price and total per share in the dict
        share_info = lookup(row["symbol"])
        row["name"] = (share_info["name"])
        row["price"] = (usd(float(share_info["price"])))
        row["total"] = (usd(float(row["shares"]) * float(share_info["price"])))
        total += (float(row["shares"]) * float(share_info["price"]))

    #put the dollar sign
    cash = usd(cash)
    total = usd(total)
    return render_template("index.html", rows = rows, cash = cash, total = total)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:
        #declare Variables and get the info
        #get username
        username = db.execute("SELECT username FROM users WHERE id = :id",
                    id = session["user_id"])[0]["username"]

        # look the info about the share, if its mistyped return error
        symbol = request.form.get("symbol")
        shareinfo = lookup(symbol)
        if not shareinfo:
            return apology("Symbol doesn't exist")
        shareprice = shareinfo["price"]

        #get the amount of shares the user wants to buy and make sure they are positive
        shareamount = request.form.get("shares")
        if not shareamount:
            return apology("You did not succeed in typing a number in the 'shares' field")
        # workaround because if you make shareamount an int before it can give an error when declaring
        shareamount = int(shareamount)
        if shareamount < 0:
            return apology("You can't buy a negative amount of shares")

        #Calculate the price for the requested amount of shares
        cashneeded = shareamount*shareprice

        #check the users budget for the transaction
        usercash = db.execute("SELECT cash FROM users WHERE id = :id",
                                id = session["user_id"])[0]["cash"]
        cashnew = usercash - cashneeded
        # if true the user cant afford the transaction
        if cashnew < 0:
            return apology("You can't afford this purchase ... yet")

        #add shares either in a new row, or amend it if one already exists for this user and share
        rows = db.execute("SELECT shares FROM shares WHERE username = :username AND symbol = :symbol",
                    username = username, symbol = symbol)

        #if the user doesnt have a share yet, add a table row, else add the extra shares, and finally update budget
        if len(rows) != 1:
            db.execute("INSERT INTO shares (username, symbol, shares) VALUES (:username, :symbol, :shares)",
                    username = username, symbol = symbol, shares = shareamount )
        else:
            shares_new = rows[0]["shares"] + shareamount
            db.execute("UPDATE shares SET shares = :shares WHERE username = :username AND symbol = :symbol",
                    shares = shares_new, username = username, symbol = symbol)
        #change budget
        db.execute("UPDATE users SET cash = :cashnew WHERE id = :id",
                    cashnew=cashnew, id = session["user_id"])

        #save information about the transaction for history, automatically adds datetime in the table
        db.execute("INSERT INTO transactions (username, symbol, shares, price, totalprice) VALUES (:username, :symbol, :shares, :price, :totalprice)",
                    username = username, symbol = symbol, shares = shareamount, price = shareprice, totalprice = cashneeded)
        flash("Purchase succesful!")
        return redirect("/")


@app.route("/history")
@login_required
def history():
    username = db.execute("SELECT username FROM users WHERE id = :id",
                id = session["user_id"])[0]["username"]
    rows = db.execute("SELECT * FROM transactions WHERE username = :username",
                username = username)

    return render_template("history.html", rows = rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")
    else:
        # get symbol and lookup details
        value = lookup(request.form.get("symbol"))
        if value == None:
            return apology("Symbol doesn't exist")
        else:
            return render_template("quoted.html", value = value)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
        # otherwise its Post, and the info needs to be saved to the db
    else:
        """get the form info and save it"""
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # if the fields are blank give error
        if not username:
            return apology("You did not succeed in typing your username")
        elif not password:
            return apology("Please try to guess your password")
        #if passwords dont match give error
        elif password != confirmation:
            return apology("Your passwords don't match... Please contact customer service for tips to hack this account")

        #hash the password
        hashpw=generate_password_hash(request.form.get("password"))

        dbname = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                            username=username,
                            hash=hashpw)
        # if name taken, apology
        if not dbname:
            return apology("name already taken")

    flash("Account created succesfully!")

    return redirect("/")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        username = db.execute("SELECT username FROM users WHERE id = :id",
                    id = session["user_id"])[0]["username"]

        # look the info about the share, if its mistyped return error
        symbol = request.form.get("symbol")
        shares_sell = int(request.form.get("shares"))
        shareinfo = lookup(symbol)
        if not shareinfo:
            return apology("That symbol doesn't exist :(")

        #check how many shares the user has and if he has enough to sell the desired amount
        shares_current = db.execute("SELECT shares FROM shares WHERE username = :username AND symbol = :symbol",
                    username = username, symbol = symbol)[0]["shares"]
        if shares_sell > shares_current:
            return apology("you don't have that many shares")
        shares_new = shares_current - shares_sell

        #change the amount of stocks
        db.execute("UPDATE shares SET shares = :shares WHERE username = :username AND symbol = :symbol",
                    shares = shares_new, username = username, symbol = symbol)

        #add the new balance
        cash_current = db.execute("SELECT cash FROM users WHERE username = :username",
                    username = username)[0]["cash"]
        shareprice = shareinfo["price"]
        totalprice = shares_sell * shareprice
        cash_new = cash_current + totalprice

        db.execute("UPDATE users SET cash = :cash WHERE username = :username",
                    cash = cash_new, username = username)

        # add everything to transactions history table

        db.execute("INSERT INTO transactions (username, symbol, shares, price, totalprice) VALUES (:username, :symbol, :shares, :price, :totalprice)",
                    username = username, symbol = symbol, shares = -shares_sell, price = shareprice, totalprice = totalprice)

        flash("Sold succesfully!")
        return redirect("/")

    else:
        return render_template("sell.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
