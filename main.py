import sqlite3
from tabulate import tabulate

connecting = sqlite3.connect('database.db')

cursor = connecting.cursor()

def create_table():
    cursor.execute('CREATE TABLE IF NOT EXISTS `cinema` (id INTEGER PRIMARY KEY , name TEXT , address TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS `movie`(id INTEGER PRIMARY KEY , name TEXT , genre TEXT , year INTEGER, description TEXT , rating REAL)')
    cursor.execute('CREATE TABLE IF NOT EXISTS `afisha` (id INTEGER PRIMARY KEY , movie_id INTEGER, cinema_id INTEGER, price INTEGER, date DATE, time TIME, capacity INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS `place`(id INTEGER PRIMARY KEY , afisha_id INTEGER , room INTEGER, row INTEGER, seat INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS `ticket`(id INTEGER PRIMARY KEY , name TEXT, phone TEXT, place_id INTEGER) ')
    cursor.execute('CREATE TABLE IF NOT EXISTS `orders`(id INTEGER PRIMARY KEY , name_film TEXT, phone TEXT, address TEXT , place_id INTEGER , date TEXT, cost INTEGER)')

create_table()
connecting.commit()

class Moviemanager:
    def __init__(self, db_name):
        self.db_manager = DatabaseManager(db_name)
        self.genres = {
            1: 'Drama',
            2: 'Crime',
            3: 'Action',
            4: 'Biografi',
            5: 'Adventure',
            6: 'Comedy',
            7: 'Animation',
            8: 'Horror',
            9: 'Mystery',
            10:'Western'
        }
        self.choice_move = None
        
    def choice(self):
        while True:
            try:
                choice = int(input('What you want do 1) Choice film 2) Use filter: '))
                if choice > 2:
                    print('You have only 2 choices')
                    continue
                else:
                    return choice
            except (TypeError, ValueError):
                print('You can only use the numbers that are shown in the list, or use the suggested filters')
                continue

    def filter_movies(self):
        while True:
            try:
                choice_filter = int(input('Use filter: 1)Drama 2)Crime 3)Action 4)Biografi 5)Adventure 6)Comedy 7)Animation 8)Horror 9)Mystery 10)Western '))
                if choice_filter < 11:
                    self.db_manager.filter_move(self.genres[choice_filter])
                    break
                else:
                    print('You can t choice more than 10')
                    continue
            except (TypeError, ValueError, FileNotFoundError):
                print('Please enter string data')
                continue


    def choice_movie(self):
        self.db_manager.choice_move_read()
        self.choice_move = int(input('Choice film: '))

        self.db_manager.choice_move(self.choice_move)
    def get_choice_move(self):
        return self.choice_move


    def pusk(self):

            choice = self.choice()

            if choice == 1:
                self.choice_movie()

            elif choice == 2:
                self.filter_movies()


class Cinemachoice:
    def __init__(self, db_name):
        self.db_manager = DatabaseManager(db_name)
        self.choice_cinema = None
        self.choice_move = None

        

    def read_cinema(self):
        self.db_manager.choice_cinema_read()

    def choise_cinema(self):
        
        while True:
            try:

                self.choice_cinema = int(input(f'Here choose the cinema that will be convenient for you to visit : '))
            except(TypeError,ValueError):

                print('You can only use the numbers that are shown in the list')

                continue
            if self.choice_cinema < 6:
                self.choice_move = Moviemanager('database.db')
                self.db_manager.choice_cinema(self.choice_cinema)
                print('OK , you choice cinema , now choice film')
                self.choice_move.pusk()
                num = self.choice_move.get_choice_move()
                self.db_manager.show_afisha(num, self.choice_cinema)
                while True:
                    try:
                    
                        self.ticket = int(input('Good , look to afisha and choice which afisha suits you best (pleace enter only num) ? :  '))
                        
                    except(TypeError,ValueError):
                        print('You can only use the numbers that are shown in the list')
                        continue
                    if self.ticket is None:
                        self.ticket = int(input('Please enter a valid ticket number: '))
                    else:
                        if self.ticket < 101:
                            
                            self.db_man = DatabaseManager('database.db')
                            self.db_man.show_choice_place()
                            name_film = self.db_man.get_name_film()
                            self.choice_place  = int(input('Next choice where you want seat , pleace give afisha_id : '))
                            self.db_man.choice_place(self.choice_place)
                            self.db_man.give_ticket(name_film , 1293, 'dsfsgr' , 12 , '2024-04-21' , 1200 , self.ticket)

                        else:
                            print('I say  enter only catergory num ')
                            continue
            else:
                print('You have only 5 choices')


                continue


    

    def push(self):
        self.read_cinema()
        self.choise_cinema()


class DatabaseManager:
    def __init__(self, db_name):
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()
        self.response = None


    def choice_cinema_read(self):
        query = 'SELECT * FROM cinema'
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        lists = [[str(rown)[:30] for rown in row] for row in response]
        head = ['num' , 'name' , 'address']
        tab = tabulate(lists, headers=head, numalign='left' ,stralign="center",tablefmt="fancy_grid")
        print(tab)

    def choice_cinema(self, id_cinema):
        query = f'SELECT name FROM cinema WHERE "ID"={id_cinema}'
        self.cursor.execute(query)
        name=self.cursor.fetchall()
        name = ', '.join([row[0] for row in name])
        adress = f'SELECT address FROM cinema WHERE "ID"={id_cinema}'
        self.cursor.execute(adress)
        adress = self.cursor.fetchall()
        adress = ', '.join([row[0] for row in adress])
        self.db.commit()
        print(f'You choice cinema with name {name} and with adress {adress}')

    def choice_move_read(self):
        query = 'SELECT * FROM movie'
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        lists = [[str(rown)[:30] for rown in row] for row in response]
        head = ['num','name' , 'ganer' ,'year' , 'description' ,'rating']
        tab = tabulate(lists, headers=head, numalign='left' ,stralign="center",tablefmt="fancy_grid")
        print(tab)

    def filter_move(self, ganer):
        query = f"SELECT * FROM movie WHERE genre = '{ganer}' "
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        lists = [[str(rown)[:30] for rown in row] for row in response]
        head = ['num','name' , 'ganer' ,'year' , 'description' ,'rating']
        tab = tabulate(lists, headers=head, numalign='left' ,stralign="center",tablefmt="fancy_grid")
        print(tab)
    def choice_move(self, id_move):
        query = f'SELECT name FROM movie WHERE "ID"={id_move} '
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        self.response = ', '.join([row[0] for row in response])
        print(f'You choice film with name {self.response}')
    
    def get_name_film(self):
        return self.response

    
    
    def show_afisha(self , move_id , cinema_id):
        query = f'SELECT * FROM afisha WHERE movie_id = {move_id} AND cinema_id = {cinema_id}'
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        if response == []:
            query = f'SELECT * FROM afisha WHERE movie_id = {move_id}'
            self.cursor.execute(query)
            response = self.cursor.fetchall()
            lists = [[str(rown)[:30] for rown in row] for row in response]
            head = ['num','movie_id' , 'cinema_id' ,'price' , 'date' ,'time' , 'capacity']
            tab = tabulate(lists, headers=head, numalign='left' ,stralign="center",tablefmt="fancy_grid")
            print('At the moment, these theaters do not have the movies you need, check out other options ')
            print(tab)
        else:
            lists = [[str(rown)[:30] for rown in row] for row in response]
            head = ['num','movie_id' , 'cinema_id' ,'price' , 'date' ,'time' , 'capacity']
            tab = tabulate(lists, headers=head, numalign='left' ,stralign="center",tablefmt="fancy_grid")
            print(tab)


    def show_choice_place(self):
        query = f'SELECT * FROM place'
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        lists = [[str(rown)[:30] for rown in row] for row in response]
        head = ['afisha_id','room' , 'row' ,'seat' ]
        tab = tabulate(lists, headers=head, numalign='left' ,stralign="center",tablefmt="fancy_grid")
        print(tab)

    def choice_place(self , afisha_id):
        
        query = f'SELECT * FROM place WHERE afisha_id = {afisha_id}'
        # ticket_id = db_manager.get_ticket_id()
        # print(ticket_id)
        # if ticket_id is not None:
        #     up = f'UPDATE afisha SET capacity = capacity - 1 WHERE "ID" = {db_manager.ticket}'
        #     self.cursor.execute(up)
        #     self.db.commit()
        # else:
        #     print("Error not found ticket ID.")
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        lists = [[str(rown)[:30] for rown in row] for row in response]
        head = ['afisha_id','room' , 'row' ,'seat' ]
        tab = tabulate(lists, headers=head, numalign='left' ,stralign="center",tablefmt="fancy_grid")
        print(f'OK , you choice place with afisha id {afisha_id} \n {tab}')


    def give_ticket(self, name_film , phone ,address ,place_id ,date , cost , ticket_id):
        db_manager = Cinemachoice('database.db')

        # if ticket_id is not None:
        up = f'UPDATE afisha SET capacity = capacity - 1 WHERE "ID" = {ticket_id}'
        self.cursor.execute(up)
        self.db.commit()
        # else:

        query = f'INSERT INTO orders (name_film, phone, address, place_id, date, cost) VALUES ("{name_film}", "{phone}", "{address}", {place_id}, {date}, {cost}); '
        self.cursor.execute(query)
        self.db.commit()

        responce = f'SELECT * FROM orders'
        self.cursor.execute(responce)
        response = self.cursor.fetchall()
        lists = [[str(rown)[:30] for rown in row] for row in response]
        head = ['name_film','phone' , 'address' ,'place_id' , 'date' , 'cost' ]
        tab = tabulate(lists, headers=head, numalign='left' ,stralign="center",tablefmt="fancy_grid")
        print(tab)





while True:
    try:
        menu = int(input(f'Hello my friend , you on cinema_ticets cait.Choice what you want do : \n 1) Choice cinema where you will watch film\n 2) See what movies are available at the box office \n 3) My Orders \n  '))
    except(TypeError,ValueError):
        print('You can use only integer , if you need use other I say about it ')
        continue
    if menu == 1:
        db_manager = Cinemachoice('database.db')
        db_manager.push()
        


    elif menu == 2: 
        while True:
            choice_move = Moviemanager('database.db')
            choice_move.pusk()
    else:
        print('You have only 3 choice')
            







