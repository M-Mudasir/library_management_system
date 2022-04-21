import sqlite3


def creating_users_table():
    conn = sqlite3.connect("UsersDB.db")
    # create a cursor
    cursor = conn.cursor()
    # create a Table
    cursor.execute("""CREATE TABLE Users(
       member_id INTEGER PRIMARY KEY,
       member_name,
       check_out,
       reserved
    )""")
    # NULL INT REAL TEXT BLOB
    # commit our command
    conn.commit()
    # close our connection
    conn.close()
    # Query the data and return ALL records


def creating_books_table():
    conn = sqlite3.connect("BooksDB.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE BooksInfo (
           book_id INTEGER PRIMARY KEY,
           title TEXT NOT NULL,
           author TEXT NOT NULL,
           sub TEXT NOT NULL,
           pub_date TEXT NOT NULL,
           check_out,
           reserved
        )""")
    conn.commit()
    conn.close()


def show_all():
    conn = sqlite3.connect("BooksDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, * FROM BooksInfo")
    items = cursor.fetchall()
    conn.commit()
    conn.close()
    return items


# ADD a single RECORD
def add_one(title, author, sub, pub_date, check_out="TRUE", reserved="FALSE"):
    conn = sqlite3.connect("BooksDB.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO BooksInfo "
                   "(title,author,sub,pub_date,check_out,reserved) "
                   "VALUES (?,?,?,?,?,?)",
                   (title, author, sub, pub_date, check_out, reserved))
    conn.commit()
    conn.close()


# Delete func
def delete_one(book_id):
    try:
        conn = sqlite3.connect("BooksDB.db")
        cursor = conn.cursor()
        cursor.execute("DELETE from BooksInfo WHERE book_id= (?)", (book_id,))
    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    conn.commit()
    conn.close()


# Add many
def populate_books_table(list):
    conn = sqlite3.connect("BooksDB.db")
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO BooksInfo "
                       "(title,author,sub,pub_date,check_out,reserved) "
                       "VALUES (?,?,?,?,?,?)", list)
    conn.commit()
    conn.close()


# searching with Where
def book_lookup(x, name):
    try:
        category = x
        print(category.upper())
        name = name
        print(name)
        conn = sqlite3.connect("BooksDB.db")
        cursor = conn.cursor()
        query = "SELECT * from BooksInfo WHERE " + category + "= (?)"
        cursor.execute(query, (name,))
        items = cursor.fetchall()
        display_pattern(items)
        conn.commit()
        conn.close()
    except Exception as error:
        print("something went wrong", error)


def display():
    conn = sqlite3.connect("BooksDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BooksInfo")
    items = cursor.fetchall()
    new_items = search_algo(items)
    display_pattern(new_items)
    conn.commit()
    conn.close()


def update(field, item, id):
    conn = sqlite3.connect("BooksDB.db")
    cursor = conn.cursor()
    # update records:
    field = field
    item = item
    item = "'" + item + "'"
    id = str(id)
    query = "UPDATE BooksInfo SET " + field + "=" + item + "  WHERE booK_id = " + id
    cursor.execute(query)
    conn.commit()
    conn.commit()
    conn.close()


def display_pattern(items):
    fields = ["ID of the book: ", "Title Of The Book: ",
              "Author Of The Book: ", "Subject Of The Book: ",
              "Publication Date of the Book: ", "Checkout status: ",
              "Reserved Status: "]
    count = 0
    for item in items:
        print("* " * 10)
        for value in item:
            print(f"{count+1}) {fields[count]} \n\t\t{value}")
            count += 1
        count = 0
        print()


def check_availability(dic_book, book_id):
    dic_book = dic_book
    count = 0
    check = None
    for key, value in dic_book.items():
        if key == book_id:
            check = value[0]
            count += 1

    if count == 0:
        print("No Book Registered under the given details")
    count = 0
    if check == "TRUE":
        return True
    else:
        return False


def check_reservation(dic_book, book_id):
    res = None
    dic_book = dic_book
    count = 0
    for key, value in dic_book.items():
        if key == book_id:
            res = value[1]
            count += 1
    if count == 0:
        print("No Book Registered under the given details")
    count = 0
    if res == "FALSE":
        return [True, res]
    else:
        return [False, res]


def get_book_details():
    dic_book = {}
    conn = sqlite3.connect("BooksDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * from BooksInfo")
    items = cursor.fetchall()
    for item in items:
        dic_book[item[0]] = [item[5], item[6]]
    conn.commit()
    conn.close()
    return dic_book


def dic_update(dic, id, loc, change):
    loc = int(loc)
    for key, value in dic.items():
        if key == id:
            value[loc] = change

    return dic


def search_algo(items):
    search_lst = []
    new_items = []
    for item in items:
        # add to dic
        x = item[1]
        search_lst.append(x)
    search_lst = bubble_sort(search_lst)
    for i in search_lst:
        for j in items:
            if i == j[1]:
                new_items.append(j)
    return new_items


def bubble_sort(array):
    # loop to access each array element
    for i in range(len(array)):
        # loop to compare array elements
        for j in range(0, len(array) - i - 1):
            # change > to < to sort in descending order
            if array[j] > array[j + 1]:
                # swapping elements if elements
                # are not in the intended order
                temp = array[j]
                array[j] = array[j + 1]
                array[j + 1] = temp
    return array


def update_column(dic_book):
    conn = sqlite3.connect("BooksDB.db")
    cursor = conn.cursor()
    # update records:
    for key, value in dic_book.items():
        field = "check_out"
        item = str(value[0])
        item = "'" + item + "'"
        id = str(key)
        query = "UPDATE BooksInfo SET " + field + "=" + item + "  WHERE book_id = " + id
        cursor.execute(query)
        conn.commit()
    for key, value in dic_book.items():
        field = "reserved"
        item = str(value[1])
        item = "'" + item + "'"
        id = str(key)
        query = "UPDATE BooksInfo SET " + field + "=" + item + "  WHERE book_id = " + id
        cursor.execute(query)
        conn.commit()

    conn.close()

