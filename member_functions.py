import sqlite3


def display():
    conn = sqlite3.connect("UsersDB.db")
    # create a cursor
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    items = cursor.fetchall()
    display_pattern(items)
    print("command executed successfully")
    # commit our command
    conn.commit()
    # close our connection
    conn.close()


# returns ALL records
def show_all():
    conn = sqlite3.connect("UsersDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, * FROM Users")
    items = cursor.fetchall()
    for item in items:
        print(item)
    conn.commit()
    conn.close()


# ADD a single member
def add_one(member_name, check_out=None, reserved=None):
    conn = sqlite3.connect("UsersDB.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users "
                   "(member_name,check_out,reserved) "
                   "VALUES (?,?,?)",
                   (member_name, check_out, reserved))
    conn.commit()
    conn.close()


# Add many members
def populate_users_table(list):
    conn = sqlite3.connect("UsersDB.db")
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO Users "
                       "(member_name,check_out,reserved) "
                       "VALUES (?,?,?)", list)
    conn.commit()
    conn.close()


# searching with Where
def book_lookup(x, name):
    try:
        category = x
        print(x)
        name = name
        print(name)
        conn = sqlite3.connect("UsersDB.db")
        cursor = conn.cursor()
        query = "SELECT * from Users WHERE " + category + "= (?)"
        cursor.execute(query, (name,))
        items = cursor.fetchall()
        display_pattern(items)
        conn.commit()
        conn.close()
    except Exception as error:
        print("An error occurred", error)


# Delete func
def delete_one(member_id):
    try:
        conn = sqlite3.connect("UsersDB.db")
        # create a cursor
        cursor = conn.cursor()

        cursor.execute("DELETE from Users "
                       "WHERE member_id= (?)", (member_id,))
    except sqlite3.Error as error:
        print("Failed to delete the record", error)
    # commit our command
    conn.commit()
    # close our connection
    conn.close()


def update(field, item, id):
    conn = sqlite3.connect("UsersDB.db")
    cursor = conn.cursor()
    field = field
    item = item
    item = "'" + item + "'"
    id = str(id)
    query = "UPDATE Users SET " \
            + field + "=" + item + "  WHERE member_id = " + id
    cursor.execute(query)
    conn.commit()
    print("command executed successfully")
    conn.commit()
    conn.close()


def display_pattern(items):
    fields = ["ID of the member: ", "Name of the member: ",
              "Check out: ", "Reserved: "]
    count = 0
    for item in items:
        print("* " * 10)
        for value in item:
            print(f"{count+1}{fields[count]}  \n\t\t{value}")
            count += 1
        count = 0
        print()


def check_reservation(dic_mem, member_id):
    dic_mem = dic_mem
    count = 0
    res = None
    for key, value in dic_mem.items():
        if key == member_id:
            res = value[1]
            count += 1
    if count == 0:
        print("\nNo Member present under the mentioned name")
    count = 0
    if res == "FALSE":
        return True
    else:
        return res


def check_checkout(dic_mem, member_id):
    check = None
    dic_mem = dic_mem
    count = 0
    for key, value in dic_mem.items():
        if key == member_id:
            check = value[0]
            count += 1

    if count == 0:
        print("\nNo Member present under the mentioned name")
    count = 0
    if check == "FALSE":
        return True
    else:
        return check


def get_member_details():
    dic_mem = {}
    conn = sqlite3.connect("UsersDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * from Users")
    items = cursor.fetchall()
    for item in items:
        dic_mem[item[0]] = [item[2], item[3]]
    conn.commit()
    conn.close()
    return dic_mem


def dic_update(dic, id, loc, change):
    loc = int(loc)
    for key, value in dic.items():
        if key == id:
            value[loc] = change
    print(dic)
    return dic


def update_column(dic_mem):
    conn = sqlite3.connect("UsersDB.db")
    cursor = conn.cursor()
    # update records:
    # update check_out
    for key, value in dic_mem.items():
        field = "check_out"
        item = str(value[0])
        item = "'" + item + "'"
        id = str(key)
        query = "UPDATE Users SET " + field + "=" + item +\
                "  WHERE member_id = " + id
        cursor.execute(query)
        conn.commit()

    for key, value in dic_mem.items():
        field = "reserved"
        item = str(value[1])
        item = "'" + item + "'"
        id = str(key)
        query = "UPDATE Users SET " + field + "=" + item + \
                "  WHERE member_id = " + id
        cursor.execute(query)
        conn.commit()
    conn.close()
