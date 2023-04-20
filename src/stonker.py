import sqlite3
import yfinance as yf
from datetime import datetime
import re
import os
import random


def create_users_table(cursor):
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            last_tutorial_read INTEGER DEFAULT 1
        )
    """)


def new_user(username, password):
    # Check if the "users" directory exists, and create it if it does not
    if not os.path.exists("users"):
        os.mkdir("users")

    # Check if the user's database exists, and create it if it does not
    user_db_path = os.path.join("users", f"{username}.db")
    if not os.path.exists(user_db_path):
        conn = sqlite3.connect(user_db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE balance (
                amount REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE stocks (
                symbol TEXT,
                shares INTEGER,
                price REAL,
                date TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO balance (amount) VALUES (?)
        """, (10000,))
        conn.commit()
        conn.close()

    # Check if the "user_database.db" file exists, and create it if it does not
    if not os.path.exists("user_database.db"):
        conn = sqlite3.connect("user_database.db")
        cursor = conn.cursor()
        create_users_table(cursor)
        conn.commit()
        conn.close()

    # Check if the "users" table exists, and create it if it does not
    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='users'
    """)
    if cursor.fetchone() is None:
        create_users_table(cursor)
        conn.commit()
    conn.close()

    # Add the new username and password to the "users" table
    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (username, password) VALUES (?, ?)
    """, (username, password))
    conn.commit()
    conn.close()

    print(f"New user {username} created with password {password}.")


def check_login(username, password):
    # Check if the username and password match in the "user_database" database
    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username FROM users WHERE username = ? AND password = ?
    """, (username, password))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        print("Username or password is incorrect.")
        return False
    else:
        print(f"Login successful for user {username}.")
        return True


def sell(username):
    user_db_path = os.path.join("users", f"{username}.db")
    conn = sqlite3.connect(user_db_path)
    c = conn.cursor()
    # get current stock inventory
    c.execute("SELECT * FROM stocks")
    stock_rows = c.fetchall()
    for row in stock_rows:
        print(row)
    # get stock ticker to sell
    ticker = input("Enter stock ticker to sell: ")
    # get number of shares to sell
    shares_to_sell = int(input("How many shares do you want to sell? "))
    # calculate sale price and update balance
    for row in stock_rows:
        if row[0] == ticker:
            if shares_to_sell <= row[1]:
                stock_price = check_stock_price(ticker)
                sale_price = stock_price * shares_to_sell
                current_bal = current_balance(username)
                new_balance = current_bal + sale_price
                c.execute("UPDATE balance SET amount = ? WHERE 1", (new_balance,))
                conn.commit()
                new_shares = row[1] - shares_to_sell
                if new_shares == 0:
                    c.execute("DELETE FROM stocks WHERE symbol=?", (ticker,))
                    conn.commit()
                else:
                    c.execute("UPDATE stocks SET shares = ? WHERE symbol = ?", (new_shares, ticker))
                    conn.commit()
                print(f"Sold {shares_to_sell} shares of {ticker} for {sale_price}.")
                break
            else:
                print("Not enough shares to complete sale.")
                break
    else:
        print("Stock not found in inventory.")
    conn.close()


def check_stock_price(ticker):
    stock_data = yf.Ticker(ticker).info
    return stock_data['regularMarketPrice']

def current_balance(username):
    user_db_path = os.path.join("users", f"{username}.db")
    conn = sqlite3.connect(user_db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM balance")
    balance = c.fetchone()[0]
    conn.close()
    return balance

def max_buy(username, ticker):
    balance = current_balance(username)
    stock_price = check_stock_price(ticker)
    return int(balance / stock_price)

def confirm_buy(username, ticker, shares):
    stock_price = check_stock_price(ticker)
    purchase_price = stock_price * shares
    balance = current_balance(username)
    if purchase_price > balance:
        return False
    else:
        user_db_path = os.path.join("users", f"{username}.db")
        conn = sqlite3.connect(user_db_path)
        c = conn.cursor()
        # check if stock already in inventory
        c.execute("SELECT * FROM stocks WHERE symbol = ?", (ticker,))
        stock_row = c.fetchone()
        if stock_row is not None:
            # update shares
            new_shares = stock_row[1] + shares
            c.execute("UPDATE stocks SET shares = ?, price = ?, date = ? WHERE symbol = ?", (new_shares, stock_price, datetime.now(), ticker))
        else:
            # insert new row
            c.execute("INSERT INTO stocks VALUES (?, ?, ?, ?)", (ticker, shares, stock_price, datetime.now()))
        # update balance
        new_balance = balance - purchase_price
        c.execute("UPDATE balance SET amount = ? WHERE 1", (new_balance,))
        conn.commit()
        conn.close()
        return True


def get_stock_data(ticker, start_date, end_date):
    """
    Returns a pandas dataframe of historical stock price data for a given ticker, 
    starting from start_date and ending on end_date.
    """
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data


def get_stock_volume(ticker, date):
    """
    Returns the trading volume for a given stock ticker on a given date.
    """
    stock_data = yf.Ticker(ticker).history(start=date, end=date)
    return stock_data["Volume"][0]


def get_stock_high(ticker, date):
    """
    Returns the high price for a given stock ticker on a given date.
    """
    stock_data = yf.Ticker(ticker).history(start=date, end=date)
    return stock_data["High"][0]


def get_stock_low(ticker, date):
    """
    Returns the low price for a given stock ticker on a given date.
    """
    stock_data = yf.Ticker(ticker).history(start=date, end=date)
    return stock_data["Low"][0]


def get_stock_open(ticker, date):
    """
    Returns the opening price for a given stock ticker on a given date.
    """
    stock_data = yf.Ticker(ticker).history(start=date, end=date)
    return stock_data["Open"][0]


def get_stock_close(ticker, date):
    """
    Returns the closing price for a given stock ticker on a given date.
    """
    stock_data = yf.Ticker(ticker).history(start=date, end=date)
    return stock_data["Close"][0]


def simulate_day_trading(username):
    print("Simulating trading day...\n")
    user_db_path = os.path.join("users", f"{username}.db")
    conn = sqlite3.connect(user_db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM stocks")
    stock_rows = c.fetchall()
    for row in stock_rows:
        ticker = row[0]
        current_price = check_stock_price(ticker)
        # generate random fluctuations in price
        price_change = random.uniform(-0.05, 0.05)
        new_price = current_price * (1 + price_change)
        c.execute("UPDATE stocks SET price = ?, date = ? WHERE symbol = ?", (new_price, datetime.now(), ticker))
        print(f"{ticker} price changed from {current_price} to {new_price}.")
    conn.commit()

    # generate random news
    print("\nGenerating news...\n")
    news_items = [
        "The Federal Reserve announced a rate hike today, causing stocks to tumble.",
        "Tech giant Apple unveiled a new line of products, boosting the company's stock.",
        "Economic data showed strong job growth, leading to gains in the stock market.",
        "Oil prices surged due to tensions in the Middle East, causing energy stocks to soar.",
        "A major company announced disappointing earnings, causing its stock to plummet."
    ]
    news_item = random.choice(news_items)
    print(news_item)

    # generate random buy/sell orders
    print("\nGenerating buy/sell orders...\n")
    for _ in range(5):
        action = random.choice(["buy", "sell"])
        if action == "buy":
            ticker = random.choice(["AAPL", "GOOG", "TSLA", "AMZN"])
            max_shares = max_buy(username, ticker)
            if max_shares == 0:
                continue
            shares = random.randint(1, max_shares)
            if confirm_buy(username, ticker, shares):
                print(f"Bought {shares} shares of {ticker}.")
        else:
            c.execute("SELECT symbol, shares FROM stocks")
            stock_rows = c.fetchall()
            if not stock_rows:
                continue
            row = random.choice(stock_rows)
            ticker = row[0]
            shares_to_sell = random.randint(1, row[1])
            sell(username, ticker, shares_to_sell)

    conn.commit()
    conn.close()




def create_portfolio_table(cursor):
    cursor.execute("""
        CREATE TABLE portfolio (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            shares INTEGER,
            purchase_price REAL,
            purchase_date TEXT
        )
    """)


def add_to_portfolio(username, symbol, shares, price):
    user_db_path = os.path.join("users", f"{username}.db")
    conn = sqlite3.connect(user_db_path)
    cursor = conn.cursor()

    # Check if the "portfolio" table exists, and create it if it does not
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='portfolio'
    """)
    if cursor.fetchone() is None:
        create_portfolio_table(cursor)
        conn.commit()

    # Check if the stock is already in the user's portfolio
    cursor.execute("""
        SELECT shares, purchase_price FROM portfolio WHERE symbol=?
    """, (symbol,))
    result = cursor.fetchone()
    if result is not None:
        # If the stock is already in the user's portfolio, update the shares and purchase price
        new_shares = result[0] + shares
        new_price = (result[1] + price) / 2
        cursor.execute("""
            UPDATE portfolio SET shares=?, purchase_price=? WHERE symbol=?
        """, (new_shares, new_price, symbol))
    else:
        # If the stock is not already in the user's portfolio, add it
        cursor.execute("""
            INSERT INTO portfolio (symbol, shares, purchase_price, purchase_date) VALUES (?, ?, ?, ?)
        """, (symbol, shares, price, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()


def sell_from_portfolio(username, symbol, shares_to_sell):
    user_db_path = os.path.join("users", f"{username}.db")
    conn = sqlite3.connect(user_db_path)
    cursor = conn.cursor()

    # Get the user's balance and check if they have enough shares of the stock to sell
    cursor.execute("""
        SELECT amount FROM balance
    """)
    balance = cursor.fetchone()[0]
    cursor.execute("""
        SELECT shares, purchase_price FROM portfolio WHERE symbol=?
    """, (symbol,))
    result = cursor.fetchone()
    if result is None:
        print("You do not own any shares of that stock.")
    elif shares_to_sell > result[0]:
        print("You do not have enough shares of that stock to sell.")
    else:
        # Calculate the sale price and update the user's balance
        sale_price = shares_to_sell * check_stock_price(symbol)
        new_balance = balance + sale_price
        cursor.execute("""
            UPDATE balance SET amount=?
        """, (new_balance,))

        # Calculate the new number of shares and update the portfolio
        new_shares = result[0] - shares_to_sell
        if new_shares == 0:
            cursor.execute("""
                DELETE FROM portfolio WHERE symbol=?
            """, (symbol,))
        else:
            cursor.execute("""
                UPDATE portfolio SET shares=? WHERE symbol=?
            """, (new_shares, symbol))

        # Commit the changes to the database and print a success message
        conn.commit()
        print(f"Sold {shares_to_sell} shares of {symbol} for {sale_price}.")
    conn.close()

def check_inventory(username):
    user_db_path = os.path.join("users", f"{username}.db")
    conn = sqlite3.connect(user_db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT amount FROM balance")
    balance = cursor.fetchone()[0]

    cursor.execute("SELECT symbol, shares, price, date FROM stocks")
    stocks = cursor.fetchall()

    total_value = balance
    for stock in stocks:
        symbol, shares, price, date = stock
        total_value += shares * price

    conn.close()

    return balance, stocks, total_value