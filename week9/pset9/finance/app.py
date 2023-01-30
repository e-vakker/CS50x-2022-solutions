import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, is_int

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    cash = db.execute("SELECT cash FROM users WHERE id = ?",
                      session.get("user_id"))[0]["cash"]
    total_cash = cash
    stocks = db.execute(
        "SELECT symbol FROM balance WHERE username_id = ?", session.get("user_id"))
    unique_stocks = []
    table_index = []

    for stock in range(len(stocks)):
        if stocks[stock]["symbol"]:
            unique_stocks.append(stocks[stock]["symbol"])

    for i in range(len(unique_stocks)):
        buffer_table = {}
        buffer_table["stocks"] = unique_stocks[i]
        buffer_table["numbers_of_shares"] = db.execute(
            "SELECT shares FROM balance WHERE username_id = ? AND symbol = ?", session.get("user_id"), unique_stocks[i])[0]["shares"]
        price = lookup(unique_stocks[i])["price"]
        buffer_table["price"] = usd(price)
        buffer_table["total_price"] = usd(
            round(float(buffer_table["numbers_of_shares"]) * float(price), 2))
        total_cash = usd(
            total_cash + round(float(buffer_table["numbers_of_shares"]) * float(price), 2))
        table_index.append(buffer_table)

    return render_template("index.html", cash=usd(cash), table_index=table_index, total_cash=total_cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == ("POST"):

        if not request.form.get("symbol"):
            return apology("Must provide symbol", 400)
        elif not request.form.get("shares"):
            return apology("Must provide shares", 400)
        elif not lookup(request.form.get("symbol")):
            return apology("Please enter right query", 400)
        elif is_int(request.form.get("shares")) != True:
            return apology("Enter a right number", 400)
        elif int(request.form.get("shares")) <= 0:
            return apology("Enter a positive number", 400)

        user_cash = db.execute(
            "SELECT cash FROM users WHERE id = ?", session.get("user_id"))[0]["cash"]
        query = lookup(request.form.get("symbol"))
        symbol = query["symbol"]
        price_of_symbol = query["price"]
        price_of_order = round(price_of_symbol, 2) * \
            int(request.form.get("shares"))
        operation = "buy"

        if user_cash < price_of_order:
            return apology("You do not have enough money for this operation", 403)

        new_user_cash = user_cash - round(price_of_order, 2)
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   round(new_user_cash, 2), session.get("user_id"))
        db.execute("INSERT INTO orders (username_id, symbol, shares, price, operation) VALUES (?, ?, ?, ?, ?)",
                   session.get("user_id"), symbol, int(request.form.get("shares")), price_of_symbol, operation)

        сhecking_stock = db.execute("SELECT symbol FROM balance WHERE username_id = ? AND symbol = ?",
                                    session.get("user_id"), symbol)

        if len(сhecking_stock) < 1:
            db.execute("INSERT INTO balance (username_id, symbol, shares) VALUES (?, ?, ?)",
                       session.get("user_id"), symbol, int(request.form.get("shares")))
        else:
            count_shares = int(db.execute("SELECT shares FROM balance WHERE username_id = ? AND symbol = ?", session.get(
                "user_id"), symbol)[0]["shares"])
            new_count = count_shares + int(request.form.get("shares"))
            db.execute("UPDATE balance SET shares = ? WHERE username_id = ? AND symbol = ?",
                       new_count, session.get("user_id"), symbol)

        return redirect("/")
    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute(
        "SELECT * FROM orders WHERE username_id = ? ORDER BY timestamp DESC", session.get("user_id"))

    return render_template("history.html", history=history)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

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
    """Get stock quote."""
    if request.method == "POST":
        symbol = lookup(request.form.get("symbol"))
        if not request.form.get("symbol"):
            return apology("Please enter your query", 400)
        elif not symbol:
            return apology("Please enter right query", 400)
        price = usd(symbol["price"])
        return render_template("quoted.html", symbol=symbol, price=price)
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Checking user input for blank input or if the user is already in the database
        if not request.form.get("username"):
            return apology("Must provide username", 400)
        elif db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username")):
            return apology("User already exists", 400)
        elif not request.form.get("password"):
            return apology("Must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("Must provide repeat password", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do NOT match", 400)

        # Inserting user name and password hash into the database
        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"))
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    list_of_stocks = db.execute(
        "SELECT symbol FROM balance WHERE username_id = ?", session.get("user_id"))
    # Querying the list of shares of the active user
    if request.method == "GET":
        return render_template("sell.html", list_of_stocks=list_of_stocks)
    # Selling
    if request.method == "POST":
        shares = request.form.get("shares")
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Must provide symbol", 400)
        elif not shares:
            return apology("Must provide shares", 400)
        elif is_int(shares) != True:
            return apology("Enter a correct number", 400)
        elif int(request.form.get("shares")) <= 0:
            return apology("Enter a positive number", 400)
        elif db.execute("SELECT symbol FROM balance WHERE username_id = ? AND symbol = ?", session.get("user_id"), symbol)[0]["symbol"] != symbol:
            return apology("Wrong symbol", 400)

        number_of_shares = db.execute(
            "SELECT shares FROM balance WHERE username_id = ? AND symbol = ?", session.get("user_id"), symbol)[0]["shares"]
        query = lookup(symbol)
        price_of_symbol = query["price"]
        price_of_order = round(price_of_symbol, 2) * int(shares)
        operation = "sell"
        user_cash = db.execute(
            "SELECT cash FROM users WHERE id = ?", session.get("user_id"))[0]["cash"]

        if int(shares) > number_of_shares:
            return apology("You don't have enough shares to sell", 400)

        db.execute("INSERT INTO orders (username_id, symbol, shares, price, operation) VALUES (?, ?, ?, ?, ?)",
                   session.get("user_id"), symbol, int(shares), price_of_symbol, operation)

        if int(shares) == number_of_shares:
            db.execute("DELETE FROM balance WHERE username_id = ? AND symbol = ?", session.get(
                "user_id"), symbol)
        else:
            new_count = number_of_shares - int(shares)
            db.execute("UPDATE balance SET shares = ? WHERE username_id = ? AND symbol = ?",
                       new_count, session.get("user_id"), symbol)

        new_user_cash = user_cash + round(price_of_order, 2)
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   round(new_user_cash, 2), session.get("user_id"))

        return redirect("/")


@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        password = db.execute(
            "SELECT hash FROM users WHERE id = ?", session.get("user_id"))

        if not request.form.get("oldpassword"):
            return apology("Must provide old password", 400)
        elif not request.form.get("newpassword"):
            return apology("Must provide new password", 400)
        elif not request.form.get("confirmation"):
            return apology("You didn't repeat the password", 400)
        elif len(password) != 1 or not check_password_hash(password[0]["hash"], request.form.get("oldpassword")):
            return apology("Wrong old password", 403)
        elif request.form.get("newpassword") != request.form.get("confirmation"):
            return apology("New password and confirmation do not match", 400)
        elif check_password_hash(password[0]["hash"], request.form.get("newpassword")):
            return apology("The old and new passwords match", 400)

        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(
            request.form.get("newpassword")), session.get("user_id"))

        return redirect("/")

    return render_template("changepassword.html")
