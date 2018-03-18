import sqlite3


def getNames():
    a = sqlite3.connect('database.db')
    c = a.cursor()
    c.execute('SELECT ID FROM {table}'.format(table='WhiteList'))
    data = c.fetchall()
    white = []
    for name in data:
        white.append(name)
    return white
