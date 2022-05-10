import sqlite3


def getdefinition(word):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    result = cur.execute(f"""SELECT def FROM defs WHERE word = '{word}'""").fetchall()
    if result == []:
        return None
    else:
        return result[0][0]


print(getdefinition('Нота'))
