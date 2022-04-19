
from getpass import getpass


class LibraryMenu:
    def __init__(self):
        self.user = None
        self.Library = Menu()
        self.action = None
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

    def run(self):
        self.login()

        while True:
            self.Library.display_menu()
            decision = str(self.validate_int())
            usr = ""
            if self.user == Type.Librarian:
                usr = "l"
            elif self.user == Type.Reader:
                usr = "r"
            decision = usr + decision
            action = self.choices.get(decision)
            if action:
                action()
            else:
                print("{} is not a valid choice".format(decision))

    def login(self):
        logged = False
        for i in range(3):
            print("Wpisz swoje ID(login): ")
            login = str(self.validate_bid())
            print("Podaj hasło: ")
            p = str(getpass("Password >>"))
            proba = 2 - i

            self.user = self.Library.login(login, p)

            if self.user is not None:
                logged = True

            if not logged:
                print("Nie udało się zalogowac, spróbuj ponownie, masz jeszcze {} próby".format(proba))
            else:
                break

        if not logged:
            print("nie udało się zalogować w 3 próbach, nastąpi wyjście z menu")
            exit()

    def add_book(self):
        print("Wprowadź tytuł książki: \n \t")
        title = self.validate_string()
        print("Wprowadź autora książki: \n \t")
        author = self.validate_string()
        while True:
            print("Wprowadź ID książki: \n \t")
            bid = str(self.validate_bid())
            if not self.Library.if_used_bid(bid):
                break
            print("Podane id jest juz w bazie, prosze podać unkatowe id(login)")
        keywords = {}
        print("Wprowadź słowo kluczowe dla książki: \n \t")
        keyword = self.validate_string()
        keywords[keyword] = {}
        while True:
            print("chcesz dodać kolejne słowo kluczowe?")
            decission = self.validate_y_n()
            if decission == 1:
                print("Wprowadź słowo kluczowe dla książki: \n \t")
                keyword = self.validate_string()
                keywords[keyword] = {}
            elif decission == 0:
                break
            else:
                print("podaj 1 lub 0 ")
        self.Library.add_book(bid, title, author, keywords)

    def delete_book(self):
        print("Podaj id książki którą chcesz usunąć")
        bid = str(self.validate_bid())
        print("Czy na pewno chcesz usunąć książkę o id  = {}?".format(bid))
        decission = self.validate_y_n()
        if decission == 1:
            self.Library.delete_book(bid)

    def show_books(self):
        self.Library.show_books()

    def add_user(self):
        print("Jakiego użytkownika chcesz dodać? \n ")
        print("""
            1. Dodaj pracownika biblioteki
            2. Dodaj czytelnika
        """)
        while True:
            decision = self.validate_int()
            if decision == 1:
                u_type = Type.Librarian
                self.place_user(u_type)
                break
            elif decision == 2:
                u_type = Type.Reader
                self.place_user(u_type)
                break
            else:
                print("Podano złą cyfrę, wybierz 1 lub 2")

    def place_user(self, u_type):
        print("Podaj imię użytkownika")
        firstname = self.validate_string()
        print("Podaj nazwisko użytkownika")
        lastname = self.validate_string()
        while True:
            print("Podaj ID(login) użytkownika")
            user_id = str(self.validate_bid())
            if not self.Library.if_used_id(user_id):
                break
            print("Podane id jest juz w bazie, prosze podać unkatowe id(login)")
        print("Ustaw hasło dla użytkownika")
        password = self.validate_string()
        self.Library.place_user(u_type, user_id, password, firstname, lastname)

    def show_users(self):
        self.Library.show_users()

    def search_book(self):
        print("Wybierz sposób przeszukiwania? \n ")

        results = []
        while True:
            print("""
                   1. Wyszukaj przez tutuł
                   2. Wyszukaj przez autora
                   3. Wyszukaj przez słowa kluczowe
               """)
            decision = self.validate_int()
            if decision == 1:
                print("Wybrano opcje wyszukiwanie po tytule. Wpisz tytuł który chcesz znaleźć:")
                print("Wpisz szukany tytuł\n uwaga tytuł musi być kompletny i poprawnie napisany \n \t")
                title = self.validate_string()
                results = self.Library.search_title(title)
            elif decision == 2:
                print("Wybrano opcje wyszukiwanie po autorze. Wpisz autora którego książki chcesz znaleźć: \n \t")
                author = self.validate_string()
                results = self.Library.search_author(author)
            elif decision == 3:
                print("Wybrano opcje wyszukiwanie po słowach kluczowych. Wpisz słowo kluczowe które cię interesuje: \n \t")
                word = self.validate_string()
                results = self.Library.search_keywords(word)
            else:
                print("Nie ma takiej opcji, wybierz i wpisz z możliwych opcji: 1 , 2, 3")

            if len(results) != 0:
                print("Pasujące wyniki wyszukiwania to: ")
                for result in results:
                    print(result)
            else:
                print("Brak pozycji dla zadanego wyszukiwania! \n")

            print("Chcesz kontynuowac przeszukiwanie?")

            want_continue = self.validate_y_n()

            if want_continue == 0:
                break
            else:
                print("Podano złą cyfrę, wybierz 1 lub 0")

    def get_return(self):
        print("Wpisz ID zwracanej książki: ")
        bid = str(self.validate_bid())
        self.Library.get_return(bid)

    def loan_book(self):
        print("Wpisz ID książki którą chcesz wypożyczyć: ")
        bid = str(self.validate_bid())
        self.Library.loan_book(bid)

    def prolongate(self):
        results, i = self.Library.show_your_books()
        if len(results) == 1:
            print("Aktualnie masz jedną pozycję wypożyczoną. Wpisz 1, aby przedłużyć wypożyczenie, 0 aby anulować ")
            print(results[0])
            to_prolongate = self.validate_y_n()
            self.Library.prolongate(results, i, to_prolongate)
        elif len(results) == 0:
            print("Aktualnie nie masz wypożyczonych książek")
        else:
            print("Którą pozycję chcesz przedłużyć? Wpisz cyfrę od 1 do {}".format(i - 1))
            for res in results:
                print(res)
            to_prolongate = self.validate_int()
            self.Library.prolongate(results, i, to_prolongate)

    def quit(self):
        self.Library.quit()

    def validate_y_n(self):
        while True:
            try:
                value = int(input("Wprowadź 1(tak) lub 0(nie): "))
            except ValueError:
                print("Wprowadzono niepoprawne dane.")
                continue
            if value > 1:
                print("Wartość większa niż 1 ")
                continue
            elif value == 1:
                return 1
            elif value == 0:
                return 0
            else:
                print("wprowadzona wartość jest niepoprawna")
                continue

    def validate_int(self):
        while True:
            try:
                value = int(input("Wprowadź cyfre z zadanego przedziału: "))
            except ValueError:
                print("Wprowadzono niepoprawne dane.")
                continue
            if value < 0:
                print("Wartość mniejsza niż 0 jest niepoprawna ")
                continue
            if len(str(value)) == 0:
                print("Proszę uzupełnić pole, pole nie moze być puste")
                continue
            elif (value % 1) != 0:
                print("Wartość nie jest liczbą całkowitą")
                continue
            else:
                return value

    def validate_bid(self):
        while True:
            try:
                value = int(input("Wpisz ID: "))
            except ValueError:
                print("Wprowadzono niepoprawne dane.")
                continue

            if value < 0:
                print("Wartość mniejsza niż 0 jest niepoprawna ")
                continue
            elif len(str(value)) == 0:
                print("Proszę uzupełnić pole, pole nie moze być puste")
                continue
            elif (value % 1) != 0:
                print("Wartość nie jest liczbą całkowitą")
                continue
            else:
                return value

    def validate_string(self):
        while True:
            try:
                value = str(input(">> "))
            except ValueError:
                print("Wprowadzono niepoprawne dane.")
                continue
            if len(value) == 0:
                print("Proszę uzupełnić pole, pole nie moze być puste")
                continue
            elif len(value) < 3:
                print("Nie może krótsze niż 3 znaki")
                continue
            elif len(value) > 15:
                print("Zbyt długie")
                continue
            elif value.isnumeric():
                print("Nie może być cyfra")
                continue
            # elif not value.isalpha():
            #     print("Nie może być cyfra")
            #     continue
            else:
                return value


if __name__ == '__main__':
    from Library_Model import Menu
    from Library_Model import Type
    from Library_Model import Status
    Library1 = LibraryMenu()
    Library1.run()
    #end