import sqlite3
import datetime
import pandas as pd


def connect():
    conn = sqlite3.connect('calories.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS calorie (id INTEGER PRIMARY KEY, amount integer, food text, protein integer, date_of_entry date)')
    conn.commit()
    conn.close()


def add_entry(amount, food, protein, date_of_entry):
    conn = sqlite3.connect('calories.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO calorie VALUES (NULL, ?, ?, ?, ?)', (amount, food, protein, date_of_entry))
    conn.commit()
    conn.close()


def print_daily_report(date):
    conn = sqlite3.connect('calories.db')
    cur = conn.cursor()
    cur.execute('SELECT Sum(amount) FROM calorie WHERE date_of_entry = ?', (date, ))
    total_calories = int(cur.fetchone()[0])
    cur.execute('SELECT Sum(protein) FROM calorie WHERE date_of_entry = ?', (date, ))
    total_protein = int(cur.fetchone()[0])
    print(f'Daily Totals: {total_calories}cal, {total_protein}g')
    # TODO display calorie & protein remaining depending on current goal
    conn.close()


def print_history(date):
    conn = sqlite3.connect('calories.db')
    cur = conn.cursor()

    cur.execute('SELECT id FROM calorie WHERE date_of_entry = ?', (date, ))
    ids = cur.fetchall()

    cur.execute('SELECT amount FROM calorie WHERE date_of_entry = ?', (date, ))
    amount = cur.fetchall()

    cur.execute('SELECT food FROM calorie WHERE date_of_entry = ?', (date, ))
    food = cur.fetchall()

    cur.execute('SELECT protein FROM calorie WHERE date_of_entry = ?', (date, ))
    protein = cur.fetchall()

    conn.close()
    """
    amount = cur.fetchall() returns a list of tuples like:
    [(300,), (50,), (150,)]
    
    so we are unpacking with amount[i][0]
    """
    if len(amount) == 0:
        print('There is no data')
    else:
        data = []
        for i in range(0, len(amount)):
            row = [amount[i][0], food[i][0], protein[i][0]]
            data.append(row)
        df = pd.DataFrame(data, columns=['Cal', 'Food', 'Protein(g)'])
        from tabulate import tabulate
        print(tabulate(df, headers=df.columns, showindex=False))
        print()
        print_daily_report(datetime.date.today())

# connect()
# add_entry(175, 'chicken', 30, datetime.date(2019, 7, 27))
# add_entry(100, 'juice', 0, datetime.date(2019, 7, 27))
# print_daily_report(datetime.date.today())
