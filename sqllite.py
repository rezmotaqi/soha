import sqlite3

# sqlLite config

con = sqlite3.connect('sent.db')


def create_table():
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS done (data text)")
    con.commit()


def insert_done(iso_datetime):
    cur = con.cursor()
    cur.execute("INSERT INTO done (data) VALUES (?)", (iso_datetime,))
    con.commit()

def check_done(iso_datetime):
    cur = con.cursor()
    cur.execute("SELECT rowid FROM done WHERE data = ?", (iso_datetime,))
    data = cur.fetchone()

    if data is None:
        return False
    else:
        return True

