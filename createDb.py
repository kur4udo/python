from datetime import datetime
import sys
import mysql.connector
import socket

# Variables

action = "bla"
dt = datetime.now()
dt_date = dt.strftime("%Y-%m-%d %H:%M:%S")

if len(sys.argv) >= 4:
    db_name = sys.argv[1]
    table_name = sys.argv[2]
    action = sys.argv[3]

tgtfdb = mysql.connector.connect(
    host = "tgtfdb.ccob0gahnz8m.eu-west-1.rds.amazonaws.com",
    port="3306",
    user = "user",
    passwd = "user12345678"
)

mycursor = tgtfdb.cursor(buffered=True)

# Functions

def usage():
    print("Uage: %s database_name table_name action" % (sys.argv[0]))
    print("\nAvailable actions:")
    print("create")
    print("insert")
    print("select\n")

def check_database(db_name):
    mycursor.execute("SHOW DATABASES")
    for x in mycursor:
        if x[0] == "%s" % (db_name):
            print("Database exists")
            return 0
    print("Database does not exist")
    return 1
    
def create_database(db_name):
    if check_database(db_name):
        print("Creating database %s" % (db_name))
        mycursor.execute("CREATE DATABASE %s" % (db_name))
        print("Database created")

def check_table(db_name, table_name):
    mycursor.execute("use %s" % (db_name))
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        if x[0] == table_name:
            print("Table exists")
            return 1
    print("Table %s does not exist" % (table_name))
    return 0
    
def create_table(db_name, table_name):
    if check_table(db_name, table_name) == 0:
        print("Creating table %s" % (table_name))
        mycursor.execute("CREATE TABLE %s.%s (id INT AUTO_INCREMENT PRIMARY KEY, dt DATETIME, hostname VARCHAR(255))" % (db_name, table_name))
        print("Table created")

def insert_host(db_name, table_name):
    if check_table(db_name, table_name):
        hostname = socket.gethostname()
        sql = "INSERT INTO %s.%s (dt, hostname) VALUES ('%s', '%s')" % (db_name, table_name, dt_date ,hostname)
        mycursor.execute(sql)
        tgtfdb.commit()
        print(mycursor.rowcount, "record inserted.")
        
def select_rows(db_name, table_name):
    if check_table(db_name, table_name):
        mycursor.execute("SELECT * FROM %s.%s" % (db_name, table_name))
        result = mycursor.fetchall()
        for r in result:
            print(r)

# Main

print(dt_date)

if action == "create":
    create_database(db_name)
    create_table(db_name, table_name)
if action == "insert":
    insert_host(db_name, table_name)
if action == "select":
    select_rows(db_name, table_name)
if action == "bla":
    usage()
