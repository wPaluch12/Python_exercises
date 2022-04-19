import datetime
import pickle
from getpass import getpass
from datetime import date, timedelta
from enum import Enum


class Menu:
    def __init__(self):
        self.user = None
        self.current_user = None
        self._books = []
        self._loans = []
        self._reservations = []
        self._users = []
        self.choices = {
            "l1": self.add_user,
            "l2": self.get_return,
            "l3": self.add_book,
            "l4": self.delete_book,
            "l5": self.search_book,
            "l6": self.show_books,
            "l7": self.show_users,
            "r1": self.loan_book,
            "r2": self.prolongate,
            "r3": self.search_book,
            "l0": self.quit,
            "r0": self.quit,
        }

    def load_data(self):
        file_to_write_users = open("users.pickle", "rb")
        self._users = pickle.load(file_to_write_users)
        file_to_write_users.close()
        file_to_write_books = open("books.pickle", "rb")
        self._books = pickle.load(file_to_write_books)
        file_to_write_books.close()
        file_to_write_loans = open("loans.pickle", "rb")
        self._loans = pickle.load(file_to_write_loans)
        file_to_write_loans.close()
        file_to_write_reserv = open("reserv.pickle", "rb")
        self._reservations = pickle.load(file_to_write_reserv)
        file_to_write_reserv.close()

    def display_menu(self):
        if self.user == Type.Reader:
            return print("""
            1. Wypożycz lub zarezerwuj książkę
            2. Przedłuż wypożyczenie 
            3. Przeszukaj katalog 
            Naciśnij 0 aby wylogować
            """)
        elif self.user == Type.Librarian:
            return print("""
            1. Dodaj użytkownika
            2. Przyjmij zwrot 
            3. Dodaj książkę
            4. Usuń książkę
            5. Przeszukaj katalog
            6. Przejrzyj katalog
            7. Przejrzyj użytkowników
            Naciśnij 0 aby wylogować
            """)
        else:
            return print("nie ma takiego użytkownika")

    def add_user(self):
        pass

    def search_book(self):
        pass

    def add_book(self, bid, title, author, keywords):
        book = {"BID": bid, "title": title, "author": author, "status": Status.Avaible, "keywords": keywords}
        self._books.append(book)
        print("\n \n Książka {} została dodana".format(book))

    def if_used_bid(self, checkid):
        for book in self._books:
            if book["BID"] == checkid:
                return True
        return False

    def delete_book(self, bid):
        for book in self._books:
            if book["BID"] == bid:
                self._books.remove(book)
                print("Książka {} została usunięta".format(book))

    def show_books(self):
        for book in self._books:
            print(repr(book))

    def place_user(self, u_type, user_id, password, firstname, lastname):
        user = {"ID": user_id, "User": u_type, "password": password, "firstname": firstname, "lastname": lastname}
        self._users.append(user)

    def if_used_id(self, checkid):
        for user in self._users:
            if user["ID"] == checkid:
                return True
        return False

    def show_users(self):
        for user in self._users:
            print(repr(user))

    def search_title(self, title):
        results = []
        for book in self._books:
            if book["title"] == title:
                results.append(book)
        return results

    def search_author(self, author):
        results = []
        for book in self._books:
            if book["author"] == author:
                results.append(book)
        return results

    def search_keywords(self, key_word):
        results = []
        for book in self._books:
            if key_word in book["keywords"]:
                results.append(book)
        return results

    def get_return(self, bid):
        for loan in self._loans:
            if loan["ksiązka"]["BID"] == bid:
                for book in self._books:
                    if book["BID"] == bid:
                        book["status"] = Status.Avaible
                self._loans.remove(loan)
                print("Książka została zwrócona")

    def loan_book(self, bid):
        loan = False
        while not loan:
             # jeżeli zarezerwoana to nie można wypożyczyć, chyba że to twoja rezerwacja i książka jest już dostępna
            for reser in self._reservations:
                if bid in reser and self.current_user["ID"] in reser:
                    for book in self._books:
                        if book["BID"] == bid:
                            if book["status"] == Status.Avaible:
                                loans = {"ksiązka": book, "użytkownik": self.current_user, "wypożyczono": date.today(),
                                         "wypożyczono do": date.today() + timedelta(days=30)}
                                self._loans.append(loans)
                                book["status"] = Status.NotAvaible
                                print("Udało się wypożyczyć książkę o podanym id")
                                self._reservations.remove(reser)
                                loan = True
                            else:
                                print("Książka nie została jeszcze zwrócona")
                elif bid in reser and self.current_user["ID"] not in reser:
                    print("Książka jest zarezerwowana, nie można jej wypożyczyć")
                    loan = True
            if not loan:
                for book in self._books:
                    if book["BID"] == bid:
                        if book["status"] == Status.Avaible:
                            loans = {"ksiązka": book, "użytkownik": self.current_user, "wypożyczono": date.today(),
                                     "wypożyczono do": date.today() + timedelta(days=30)}
                            self._loans.append(loans)
                            book["status"] = Status.NotAvaible
                            loan = True
                            print("Udało się wypożyczyć książkę o podanym id")
                        elif book["status"] == Status.NotAvaible:
                            due_date = datetime.date
                            for loan_s in self._loans:
                                if loan_s["ksiązka"]["BID"] == bid:
                                    due_date = loan_s["wypożyczono do"]
                            print("Książka nie jest dostępna, jest wypożyczona do: {} ".format(due_date))
                            for my_loans in self._loans:
                                if my_loans["użytkownik"] == self.current_user and my_loans["ksiązka"] == book:
                                    print(
                                        "ta książka jest wypożyczona przez ciebie, nie możesz jej zarezerwować, możesz przedłużyć wypożyczenie!")
                                    loan = True
                                    break
                                else:
                                    print(
                                        "Czy chcesz zarezerwować książkę, jej wypożyczenie będzie możliwe dopiero po upłynięciu daty: {}".format(
                                            due_date))
                                    while True:
                                        do_reservation = str(input(" yes(1)/no(0) >>"))
                                        if do_reservation == "1":
                                            book1 = book
                                            self._reservations.append({book1["BID"]: {}, self.current_user["ID"]: {}})
                                            print("Książka została zarezerwowana")
                                            loan = True
                                            break
                                        elif do_reservation == "0":
                                            print("Ksiązka nie została zarezerowana")
                                            loan = True
                                            break
                                        else:
                                            print("wpisz 1 lub 0 -> yes(1)/no(0)")
                                    break
                print("Nie ma książki o podanym numerze")
                loan = True
                break
            if not loan:
                print("Nie udało się zarezerwowac książki o podanym id")

    def show_your_books(self):
        results = []
        i = 1
        for book in self._loans:
            if book["użytkownik"] == self.current_user:
                results.append(book)
                i += 1
        return results, i

    def prolongate(self, results, i, to_prolongate):
        if to_prolongate in range(i - 1):
            loan_to_prolongate = results[to_prolongate - 1]
            book_to_prolongate = loan_to_prolongate["ksiązka"]
            for book_longer in self._loans:
                if book_longer["ksiązka"] == book_to_prolongate:
                    book_longer["wypożyczono do"] = book_longer["wypożyczono do"] + timedelta(days=30)
                    print("Pomyślnie przedłużono książkę: {} do {}".format(book_to_prolongate["title"],
                                                                           book_longer["wypożyczono do"]))

    def login(self, login, p):
        self.load_data()
        for user in self._users:
            if user["ID"] == login:
                if user["password"] == p:
                    self.current_user = user
                    self.user = user["User"]
                    return self.user
                else:
                    return None



    def quit(self):
        file_to_write_users = open("users.pickle", "wb")
        pickle.dump(self._users, file_to_write_users)
        file_to_write_users.close()
        file_to_write_books = open("books.pickle", "wb")
        pickle.dump(self._books, file_to_write_books)
        file_to_write_books.close()
        file_to_write_loans = open("loans.pickle", "wb")
        pickle.dump(self._loans, file_to_write_loans)
        file_to_write_loans.close()
        file_to_write_reserv = open("reserv.pickle", "wb")
        pickle.dump(self._reservations, file_to_write_reserv)
        file_to_write_reserv.close()
        exit()


class Type(Enum):
    Librarian = 1
    Reader = 2


class Status(Enum):
    Avaible = 1
    Reserved = 2
    NotAvaible = 3



