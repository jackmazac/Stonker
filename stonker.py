import sqlite3
import yfinance as yf
from datetime import datetime
import re
import os


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

    # Add the new username and password to the "user_database" database
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

def check_stock_price(ticker):
    stock_data = yf.Ticker(ticker)
    current_price = stock_data.info["regularMarketPrice"]
    return current_price

def current_balance(username):
    # Get the user's balance from their database
    user_db_path = os.path.join("users", f"{username}.db")
    conn = sqlite3.connect(user_db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT amount FROM balance
    """)
    result = cursor.fetchone()
    conn.close()

    if result is None:
        print(f"User {username} not found.")
        return None
    else:
        balance = result[0]
        print(f"Current balance for {username}: ${balance:.2f}")
        return balance

def check_inventory(username):
    # Get the user's stock inventory from their database
    user_db_path = os.path.join("users", f"{username}.db")
    conn = sqlite3.connect(user_db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT symbol, shares, price, date FROM stocks
    """)
    results = cursor.fetchall()
    conn.close()

    if len(results) == 0:
        print(f"No stocks found in inventory for user {username}.")
        return []
    else:
        inventory = []
        for row in results:
            stock = {
                "symbol": row[0],
                "shares": row[1],
                "price": row[2],
                "date": row[3]
            }
            inventory.append(stock)
        print(f"Current inventory for user {username}:")
        for stock in inventory:
            print(f"{stock['symbol']}: {stock['shares']} shares @ ${stock['price']} ({stock['date']})")
        return inventory

def max_buy(username, ticker):
    #Check current stock price
    price = check_stock_price(ticker)
    print(f"Current price of {ticker}: ${price:.2f}")

    # Calculate max number of shares user can buy
    balance = current_balance(username)
    max_shares = int(balance / price)
    print(f"Max shares you can buy: {max_shares}")
    
    return max_shares


#LEFT OFF HERE
###############################

def buy(username):
    user_db_path = os.path.join("users", f"{username}.db")
    conn = sqlite3.connect(user_db_path)
    c = conn.cursor()
    # Prompt for stock ticker
    ticker = input("Enter stock ticker: ").upper()


    # Prompt user for amount of shares to buy
    shares = int(input("How many shares do you want to buy? "))
    if shares > max_shares:
        print("Insufficient balance to purchase that many shares")
        return

    # Subtract cost of shares from user balance
    cost = shares * price
    c.execute("UPDATE inventory SET balance = balance - ?", (cost,))
    conn.commit()

    # Add shares to user's portfolio
    purchase_date = datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT * FROM portfolio WHERE ticker=?", (ticker,))
    stock = c.fetchone()
    if stock:
        shares_owned = stock[2] + shares
        c.execute("UPDATE portfolio SET shares=?, purchase_date=? WHERE ticker=?", (shares_owned, purchase_date, ticker))
    else:
        c.execute("INSERT INTO portfolio VALUES (?, ?, ?, ?)", (ticker, price, shares, purchase_date))
    conn.commit()

    print(f"Purchased {shares} shares of {ticker} for ${cost:.2f}")

    conn.close()



def sell(username):
    conn = sqlite3.connect(f"database/{username}.db")
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
                stock_price = check_stock_price 
                sale_price = stock_price * shares_to_sell
                new_balance = current_balance + sale_price
                c.execute("UPDATE inventory SET money = ?", (new_balance,))
                conn.commit()
                new_shares = row[1] - shares_to_sell
                if new_shares == 0:
                    c.execute("DELETE FROM stocks WHERE ticker=?", (ticker,))
                    conn.commit()
                else:
                    c.execute("UPDATE stocks SET shares = ? WHERE ticker = ?", (new_shares, ticker))
                    conn.commit()
                print(f"Sold {shares_to_sell} shares of {ticker} for {sale_price}.")
                break
            else:
                print("Not enough shares to complete sale.")
                break
    else:
        print("Stock not found in inventory.")
    conn.close()


def tutorial(user):
    tutorial_text = [
        "Module 1: Introduction to the game",
        "Module 2: How to buy stocks",
        "Module 3: How to sell stocks",
        "Module 4: Understanding stock prices",
        "Module 5: Common trading strategies",
        "Module 6: Tips for success",
        "Module 7: How to interpret financial reports",
        "Module 8: Fundamental analysis",
        "Module 9: Technical analysis",
        "Module 10: Using options to trade stocks"
    ]
    
    # Connect to the SQL database
    conn = sqlite3.connect('database/user_inventories.db')
    c = conn.cursor()
    
    # Get the last tutorial read by the user from the database
    username = user['username']
    c.execute("SELECT last_tutorial FROM users WHERE username=?", (username,))
    last_tutorial = c.fetchone()[0]

    #Print the last tutorial read by the user
    print(f"Last tutorial read: {tutorial_text[last_tutorial-1]}")
    
    # Print the tutorial text
    for i, text in enumerate(tutorial_text):
        print(f"{i+1}. {text}")
    
    # Ask the user which module they want to read
    tutorial_num = int(input("Which tutorial module would you like to read? "))
    
    # Check that the tutorial number is valid
    if tutorial_num < 1 or tutorial_num > len(tutorial_text):
        print("Invalid tutorial number")
        return
    
    # Print the selected tutorial module
    print(f"\n{tutorial_text[tutorial_num-1]}:\n")
    print("This is the tutorial content.")
    
    # Update the user's last tutorial read in the database
    c.execute("UPDATE users SET last_tutorial=? WHERE username=?", (tutorial_num, username))
    conn.commit()
    
    # Close the database connection
    conn.close()