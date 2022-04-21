import helper
import member_functions
import time


class Admin:
    def __init__(self):
        print("\nLogged in as admin\n")
        self.choose()

    def choose(self):
        print("""How do you want to proceed ?
1. Add | Remove | Edit a book
2. Search a book
3. Edit memberships
4. Return""")
        opt = input("Your option: ")
        if opt == "1":
            print("Book Operations")
            BookOperations()
        elif opt == "2":
            print("Search a book")
            Search()
        elif opt == "3":
            print("Memberships")
            Membership()
        elif opt == "4":
            Run()
        else:
            print("Enter a correct option")
            self.choose()


class Member:

    def __init__(self):

        x = input("How do you want to proceed \n1. "
                  "Membership Details \n2. Return \nYour Option: ")
        print()
        if x == "1":
            self.dic_book = helper.get_book_details()
            self.dic_mem = member_functions.get_member_details()
            self.option()
        else:
            Run()

    def option(self):
        print()
        mem_id = int(input("Enter your ID to login: "))
        print("How do you want to proceed ")
        x = input("1. Checkout\n2. Renew\n3. "
                  "Reserve\n4. Display all books \n5. Return \nYour option: ")

        if x == "1":
            print("Checking out")
            self.check_out(mem_id)
        elif x == "2":
            self.renew()
        elif x == "3":
            self.reserve(mem_id)
        elif x == "4":
            self.display()
        elif x == "5":
            self.return_book(mem_id)

    @staticmethod
    def display():
        temp = []
        for i in helper.show_all():
            j = list(i)
            j.pop(0)
            temp.append(j)
        helper.display_pattern(temp)

    def check_out(self, mem_id):

        # first checking out that is there any book that this member have already issued
        check_m_db = member_functions.check_checkout \
            (self.dic_mem, mem_id)
        if check_m_db:
            print("\nSelect from the following Books")
            # display book
            helper.display()
            book_id = int(input("\nPlease enter the book id: "))
            # checking availability of book and checking that book isn't
            check_b_db = helper.check_availability \
                (self.dic_book, book_id)
            res_b_db = helper.check_reservation \
                (self.dic_book, book_id)
            print(check_b_db)
            print(res_b_db)
            if check_b_db == True and (True in res_b_db):
                print("Checking out")
                for i in range(3):
                    print(".")
                    time.sleep(0.2)
                # modifying the check_out field in book_db
                self.dic_book = helper.dic_update \
                    (self.dic_book, book_id, "0", mem_id)
                self.dic_mem = member_functions.dic_update \
                    (self.dic_mem, mem_id, "0", book_id)

            else:
                print("\nBook Out of Stock")
                x = input("Reserve the book (y/n)").capitalize()
                if x == "Y":
                    r = self.reserve(mem_id)

        else:
            print("\nYou have already checked out once")

        opt = input("Do you want to continue: ")
        if opt == "Y":
            self.option()
        else:
            # save that update data of dictionary to database
            self.save()
            self.__init__()

    def renew(self):
        input('Do you want to renew the book ?')
        for i in range(3):
            print(".")
            time.sleep(0.2)

        print("The book has been renewed ")
        # there is no need to make any change in the dictionary
        opt = input("Press y to continue").capitalize()
        if opt == "Y":
            self.option()
        else:
            self.save()
            self.__init__()

    def reserve(self, mem_id):
        # first checking out that is there any book that this member have already made reservation
        res_m_db = member_functions.check_reservation(self.dic_mem, mem_id)
        if res_m_db:
            print("Select from the following ")
            # display book
            helper.display()
            book_id = int(input("Please enter the Book id: "))
            # checking availability of book and checking that book is reserved
            check_b_db = helper.check_availability \
                (self.dic_book, book_id)
            res_b_db = helper.check_reservation \
                (self.dic_book, book_id)
            print("check_b_db:", check_b_db)
            print("res_b_db", res_b_db)
            if check_b_db == False and (True in res_b_db):
                print("The book is being reserved")
                for i in range(3):
                    print(".")
                    time.sleep(0.2)
                # modifying the check_out field in book_db
                self.dic_book = helper.dic_update \
                    (self.dic_book, book_id, "1", mem_id)
                self.dic_mem = member_functions.dic_update \
                    (self.dic_mem, mem_id, "1", book_id)
            else:
                if check_b_db:
                    print("The book is already available,"
                          " You don't need to reserve it. ")
                elif not res_b_db:
                    print("The book is reserved")

        else:
            print("You have already reserved a book")

        opt = input("\nDo You want to continue (y/n)?").capitalize()
        if opt == "Y":
            self.option()
        else:
            self.save()
            self.__init__()

    def save(self):
        dic_book = self.dic_book
        dic_mem = self.dic_mem

        # calling update_column function of book_db and mem_db respectively
        helper.update_column(dic_book)
        member_functions.update_column(dic_mem)
        print("Updating Data")
        for i in range(3):
            print(".")
            time.sleep(0.2)
        print("Data updated")
        opt = input("DO you want to Continue (y/n)?\n:").capitalize()
        if opt == "Y":
            self.option()
        else:
            self.save()
            self.__init__()

    def return_book(self, mem_id):
        # Taking book_id from member
        book_id = self.dic_mem[mem_id][0]
        self.dic_mem = member_functions.dic_update(self.dic_mem, mem_id, "0", "FALSE")
        # FILLING THE BOOK IN THE SLOT
        self.dic_book = helper.dic_update(self.dic_book, book_id, "0", "TRUE")
        # checking for reservations, book will be checked out to the respective member IF True THE reservation
        # becomes FALSE
        res_b_db = helper.check_reservation(self.dic_book, book_id)
        if False in res_b_db:
            res_mem_id = res_b_db[1]
            # checking_out book to that person
            self.dic_mem = member_functions.dic_update \
                (self.dic_mem, res_mem_id, "0", book_id)
            self.dic_mem = member_functions.dic_update \
                (self.dic_mem, res_mem_id, "1", "FALSE")
            self.dic_book = helper.dic_update \
                (self.dic_book, book_id, "0", res_mem_id)
            self.dic_book = helper.dic_update \
                (self.dic_book, book_id, "1", "FALSE")
        else:
            pass

        opt = input("DO you want to Continue (y/n)?\n:").capitalize()
        if opt == "Y":
            self.option()
        else:
            self.save()
            self.__init__()


class Membership():

    def __init__(self):
        self.option()

    def option(self):
        print('How do you want to proceed ? ')
        opt = input("1. Adding a new member \n2. "
                    "Cancelling a membership\n3. Return \nYour Option : ")
        if opt == "1":
            self.add_member()
        elif opt == "2":
            self.remove_member()
        elif opt == "3":
            a = Admin()
        else:
            print("Select a Valid option")
            self.option()

    def add_member(self):

        x = int(input("Enter the number of members you want to add"))
        try:
            if x == 1:
                member_name = input("Member Name:")
                member_functions.add_one(member_name)
            else:
                lst = []
                for i in range(x):
                    member_name = input("Member Name:")
                    lst.append((member_name, "FALSE", "FALSE"))
                member_functions.populate_users_table(lst)
                lst = []
        except Exception:
            print("There was an error, please try again")
            self.add_member()
        self.option()

    def remove_member(self):
        member_functions.display()
        try:
            x = input("Enter the ID of the member ")
            member_functions.delete_one(x)
        except Exception:
            print('There was an error, please try again')
            self.remove_member()
        self.option()


class Search():
    def __init__(self):
        self.search()

    def search(self):
        print("Select the searching criteria ")
        print("title || author || sub || pub_date")
        print()
        x = input("Your Option: ")
        value = input("Enter the value for searching criteria: ")
        print()
        helper.book_lookup(x, value)
        while True:
            opt = input("Do you want to continue ?\n1. Yes \n2. No")
            if opt == "1":
                self.search()
                break
            elif opt == "2":
                a = Admin()
                break
            else:
                print("Invalid selection")


class BookOperations:
    def __init__(self):
        try:
            print("""\n How do you want to proceed:
1. Add a book
2. Delete a book
3. Modify a book
4. Return """)
            option = input("Your option: ")
            if option == "1":
                self.add_book()
            elif option == "2":
                self.delete_book()
            elif option == "3":
                self.edit_info()
            else:
                a = Admin()
        except Exception as error:
            print("Some error occurred", error)

    def edit_info(self):
        helper.display()
        field = input("Enter the updating criteria ")
        id = input("Enter the book ID: ")
        item = input("Enter the updated Item ")
        helper.update(field, item, id)
        self.__init__()

    def add_book(self):

        choice = int(input("How many records do you want to insert ?"))
        print("Please input the following details ")
        if choice == 1:
            title = input("title: ")
            author = input("author: ")
            sub = input("subject: ")
            pub_date = input("publication date: ")
            helper.add_one(title, author, sub, pub_date)
        else:
            lst = []
            for i in range(choice):
                title = input("title: ")
                author = input("author: ")
                sub = input("subject: ")
                pub_date = input("publication date: ")
                lst.append((title, author, sub, pub_date, "TRUE", "FALSE"))
            helper.populate_books_table(lst)
            lst = []
        self.__init__()

    def delete_book(self):
        helper.display()
        book_id = int(input("Enter the Id of the book: "))
        helper.delete_one(book_id)
        self.__init__()
        # calling func of book_db


if __name__ == '__main__':
    class Run:
        def __init__(self):
            print("How do you want to log in as ?\n1. Admin\n2. Member\n3. Exit")
            choice = input("\nYour option: ")
            if choice == "1":
                print("Logging in as admin")
                for i in range(3):
                    print(".")
                    time.sleep(0.2)
                Admin()

            elif choice == '2':
                print("Logging in as member")
                for i in range(3):
                    print(".")
                    time.sleep(0.2)
                Member()

            else:
                quit()


    Run()
