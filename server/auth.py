import sqlite3
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash


def reset_user_password(password):
    hashPswd = generate_password_hash(password, 'sha256')
    conn = None
    c = None
    try:
        conn = sqlite3.connect('auth.db')
        c = conn.cursor()
        c.execute("UPDATE credentials SET PASSWORD=? WHERE ID=0;", (hashPswd,))
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()


def authenticate(username, password):
    if not username or not password:
        return None
    conn = None
    c = None
    try:
        conn = sqlite3.connect('auth.db')
        c = conn.cursor()
        c.execute("SELECT PASSWORD FROM credentials WHERE ID=0;")
        rows = c.fetchall()
        hashed = rows[0][0]
        user = {
            'username': 'default',
            'password': hashed
        }
    except sqlite3.Error as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()
    if not check_password_hash(hashed, password):
        return None
    return user

def activate_session(username):
    conn = None
    c = None
    try:
        conn = sqlite3.connect('auth.db')
        c = conn.cursor()
        c.execute("INSERT INTO session VALUES(?);", (username,))
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()

def deactivate_session(username):
    conn = None
    c = None
    try:
        conn = sqlite3.connect('auth.db')
        c = conn.cursor()
        c.execute("DELETE FROM session WHERE username=?;", (username,))
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()

