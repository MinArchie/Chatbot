import mysql.connector
import os


try:
    p = os.environ['PASSWD']
    mydb = mysql.connector.connect(host='localhost', user='root', password=p, database='chatbot_db')
    mycur = mydb.cursor()
except:
    p = os.environ['PASSWD']
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=p
    )
    mycur = mydb.cursor()
    mycur.execute("create database chatbot_db")
    mycur.execute("use chatbot_db")
    mycur.execute("create table holidays(date date, holiday_name "
                  "char(40) PRIMARY KEY, sl_no int unique auto_increment);")
    mydb.commit()
    mydb.close()

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=p,
        database='chatbot_db'
    )
    mycur = mydb.cursor()
    q2 = '''insert into holidays(date, holiday_name) values("2023-12-25", "Christmas"),
    ("2023-10-24", "Diwali"),
    ("2023-10-05","Dussehra"),
    ("2023-10-02", "Gandhi Jayanti"),
    ("2023-08-31", "Ganesh Chaturthi"),
    ("2022-08-15","Independence Day"),
    ("2022-11-01","Karnataka Rajyotsava"),
    ("2022-05-01","Labour Day"),
    ("2022-01-14","Makar Sankranti"),
    ("2022-01-01","New Year"),
    ("2022-04-10","Rama Navami"),
    ("2022-01-26","Republic Day"),
    ("2022-03-01","Shivratri"),
    ("2022-04-02","Ugadi")  
    ;'''
    mycur.execute(q2)
    mydb.commit()
    mydb.close()

def query_db(query):
    global my_conn
    global my_connect
    p = os.environ['PASSWD']
    my_connect = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=p,
        database="chatbot_db"
    )

    my_conn = my_connect.cursor()
    ####### end of connection ####
    my_conn.execute(query)



def view_table():
    query_db("SELECT sl_no, date, holiday_name FROM holidays order by sl_no asc;")
    i = 0
    for holiday in my_conn:
        for j in range(len(holiday)):
            print(holiday[j], end='         ')
        i = i + 1
        print()


def update_row():
    holi = input("Enter name of holiday you wish to update: ")
    new = input("Enter new date (YYYY-MM-DD): ")
    q = "update holidays set date = \'" + new + "\' where holiday_name = \'" + holi + "\' ;"
    query_db(q)
    my_connect.commit()


def insert_row():
    name = input("Insert name of holiday: ")
    date = input("Insert Date: ")
    q = "insert into holidays values(\'" + date +"\', \'" + name + "\', null);"
    query_db(q)
    my_connect.commit()


def delete_row():
    name = input("Enter name of holiday: ")

    q = "delete from holidays where holiday_name = \'" + name +"\';"
    query_db(q)
    my_connect.commit()


def main():
    while True:
        print("1) View")
        print("2) Update")
        print("3) Insert")
        print("4) Delete")
        print("5) Exit")
        ch = int(input("Enter choice: "))
        if ch == 1:
            view_table()
            print()
        elif ch == 2:
            update_row()
            print()
        elif ch == 3:
            insert_row()
            print()
        elif ch == 4:
            delete_row()
            print()
        elif ch == 5:
            break
        else:
            print("Input valid option")
            print()

main()