#code some SQL operations: 
import sqlite3
import time

def connect():
    conn = sqlite3.connect("BP.db") #BP means blood pressure
    cur = conn.cursor()
    #time is text datatype, https://tableplus.com/blog/2018/07/sqlite-how-to-use-datetime-value.html
    cur.execute("CREATE TABLE IF NOT EXISTS bp_table (id INTEGER PRIMARY KEY, time int, high int, low int)")
    conn.commit()
    conn.close()

def insert(time, high, low):
    conn = sqlite3.connect("BP.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO bp_table VALUES (NULL,?,?,?)", (time, high, low))
    conn.commit()
    conn.close()
    
def view():
    conn = sqlite3.connect("BP.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM bp_table")
    rows = cur.fetchall()
    conn.close()
    return rows

# def search(title="", author="", year="", isbn=""):
#     conn = sqlite3.connect("BP.db")
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM book WHERE title=? OR author=? OR year=? OR isbn=?", (title, author, year, isbn))
#     rows = cur.fetchall()
#     conn.close()
#     return rows

def delete(id):
    conn = sqlite3.connect("BP.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM bp_table WHERE id=?", (id,))
    conn.commit()
    conn.close()
    
def update(id, time, high, low):
    conn = sqlite3.connect("BP.db")
    cur = conn.cursor()
    cur.execute("UPDATE book SET time=?, high=?, low=? WHERE id=?", (time, high, low, id))
    conn.commit()
    conn.close()
    
# connect()    
# insert(int(time.time()), 120, 80)
#delete(3)
#update(4, "The moon", "John Smooth", 1917, 99999)
# print(view())
#print(search(author="John Smith"))

## https://csatlas.com/python-unix-timestamp/
# #unix time
# import time
# now_unix = int(time.time())
# print(now_unix)

# #datatime
# from datetime import datetime
# now = datetime.now()
# print(now)

# #convert datetime to unix time
# timestamp = int(now.timestamp())
# print(timestamp)

# convert unix to datetime
# timestamp = 1614983421
# dt = datetime.fromtimestamp(timestamp)
# print( dt )

if __name__ == '__main__':
    main()
