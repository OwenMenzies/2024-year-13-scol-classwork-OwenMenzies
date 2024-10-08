''' This is a program which allows users to manage a movie database system with seats and save beyond the current session'''
# set up imports
import sqlite3

# Set up and connect to the database
DATABASE = 'MovieManager.db'
connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()
movie_list = []
# send an initial query to attain theater data
query = "SELECT TheaterID, TheaterName, TheaterSeats FROM Theater ORDER BY TheaterID"
cursor.execute(query)
theater_cap = []
results = cursor.fetchall()


# create a list with theater data
for i in results:
    theater_cap.append([i[0], i[1], i[2]])


# Create the class of movie with an ID, name, seats left, theater name, and ID
class movie:
    # Initialize the class and its objects
    def __init__(self, movie_id, movie_name, movie_seats_left, theater_name, theater_id, movie_price, movie_time):
        self._id = movie_id
        self._name = movie_name
        self._seats = movie_seats_left
        self._theater = theater_name
        self._theater_id = theater_id
        self._movie_price = movie_price
        self._movie_time = movie_time
        self._position = len(movie_list)
        # set up a list with all the objects
        movie_list.append(self)

    # Return the individual items
    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

    def get_seats(self):
        return self._seats

    def get_theater(self):
        return self._theater

    def get_theater_id(self):
        return self._theater_id

    def get_price(self):
        return self._movie_price

    def get_time(self):
        return self._movie_time

    def get_position(self):
        return self._position

    # Decrease the seats quantity in both the object and the database
    def decrease_seats(self, quantity):
        # query = str("UPDATE MovieIndex set MovieSeatsLeft = '" + str(self._seats - quantity) + "' where MovieID == " + str(self._id))
        # query = str("UPDATE MovieIndex set MovieSeatsLeft = ? where MovieID == ?")
        cursor.execute("UPDATE MovieIndex set MovieSeatsLeft = ? where MovieID == ?",self._seats - quantity,self._id)
        self._seats -= quantity
        connection.commit()

    # Change the name in both the database and the movie list
    def change_name(self, new_name):
        # query = str("UPDATE MovieIndex set MovieName = ? where MovieID == ?")
        cursor.execute("UPDATE MovieIndex set MovieName = ? where MovieID == ?",(new_name,self._id))
        connection.commit()
        self._name = new_name

    # Remove the movie from the database and update list positions of objects
    def delete_movie_db(self):
        # Update the positions in the list for all the movies above the selected movie
        indicy = self._position
        for i in movie_list:
            if i._position >= indicy and len(movie_list) != indicy:
                i._position = i._position - 1
        # Remove the movie from the database
        
        cursor.execute("DELETE FROM MovieIndex WHERE MovieID = ?",self._id)
        connection.commit()

    # Add a movie to the database
    def add_movie(self):
        # query = "INSERT INTO MovieIndex VALUES (" + str(self._id) + ", '" + self._name + "', " + str(self._seats) + ", " + str(self._theater_id) + ", "+ str(self._movie_price) + ", " + str(self._movie_time) + ");"
        # query = "INSERT INTO MovieIndex VALUES (?,?,?,?,?,?)",(self._id,self._name,self._seats,self._theater_id,self._movie_price,self._movie_time)
        
        cursor.execute("INSERT INTO MovieIndex VALUES (?,?,?,?,?,?)",(self._id,self._name,self._seats,self._theater_id,self._movie_price,self._movie_time))
        connection.commit()
    def update_time(self,new_time):
        cursor.execute("UPDATE MovieIndex set MovieTime = ? where MovieID == ?",(new_time,self._id))
        connection.commit()
        self._movie_time = new_time


    def update_price(self,new_price):
        cursor.execute("UPDATE MovieIndex set MoviePrice = ? where MovieID == ?",(new_price,self._id))
        connection.commit()
        self._movie_time = new_price
        pass

  

# Execute movie query
query = "SELECT MovieID,MovieName,MovieSeatsLeft,TheaterName,Theater.TheaterID,MoviePrice,MovieTime FROM MovieIndex INNER JOIN Theater ON MovieIndex.MovieTheaterID = Theater.TheaterID"
cursor.execute(query)

results = cursor.fetchall()
# create movie objects 
for result in results:
    movie(result[0], result[1], result[2], result[3], result[4],result[5],result[6])


#  create a universal error checker function
def error_checker(lower=0, upper=0, data_type="int"):
    # run until a valid input is recieved  
    while True:
        # check if the integer is above the minimum and below the maximum
        if data_type == "int":
            try:
                value = int(input())
                if lower <= value <= upper:
                    return value
                else:
                    print(f"Please enter an integer between {lower} and {upper}")
            except ValueError:
                print(f"Please enter an integer between {lower} and {upper}")

        # check if the number is above the minimum and below the maximum
        if data_type == "float":
            try:
                value = float(input())
                if lower <= value <= upper:
                    return value
                else:
                    print(f"Please enter a number between {lower} and {upper}")
            except ValueError:
                print(f"Please enter a number between {lower} and {upper}")
        # check if the input is a valid time 
        if data_type == "time":
            # split into hours and minutes
            hours,minutes = input().split(":")
            hours = int(hours)
            minutes = int(minutes)
            # print (hours,minutes)
            # print(hours*60+minutes)
            # check if time follows universal principles e.g. no 11:67 am
            if hours >= 0 and hours <24 and minutes >=0 and minutes <=59:
                # print(hours,"gooder times")
                return hours*60+minutes
        
            else:
                print("Please enter a valid time") 
        # check if the string is only spaces
        # if data_type == "string":
        #     string = input()
           
        #     for i in string:
        #         if i.isspace == False:
        #             non_space = True
            
            
# allow the user to chose a theater to log in to
def theater_choser():
        while True:
            print(f"Which theater would you like to log in to? (1 for Hi Vis Jacket (80 seats), 2 for Ladder and Clipboard (120 seats), 3 for Long Trenchcoat (200 seats))")
           
            # receive the input from the user and asign it to the desired theater
            theater_id = error_checker(1, 3, "int") - 1
            theater = theater_cap[theater_id][1]

            # confirm with user if the chosen theater is correct
            print(f"Are you sure you would like to log in to {theater}? (1 for yes, 2 for no)")
            confirm = input()
            if confirm == "1":
                return theater, theater_id+1

# print the time in standard form
def print_time(minutes_after_midnight):
    return (str(minutes_after_midnight//60)+":"+str((minutes_after_midnight%60)).zfill(2))

# Display every movie in a table format
def display_all_table():
    # allow other functions to access the printed movies list 
    global printed_movies 
    printed_movies = []
    initial_print = True
   
    # print the movies 
    for i in range(len(movie_list)):

        
        if movie_list[i].get_theater() == theater:
            # check that there is at least one move and if so print the header
            if initial_print == True:
                print("Movie number - Movie name    -    Seats left - Price - Showing time")
                initial_print = False
            # print the rest of the movies formated and append it to a list of printed movies
            print(f"{len(printed_movies)+1:3}  {(movie_list[i].get_name()):30} {(movie_list[i].get_seats()):3} {(movie_list[i].get_price()):10.2f} {(print_time(movie_list[i].get_time())):10}")
            printed_movies.append(movie_list[i].get_position())

# print all movies for testing purposes
def print_all():
    print("Movie number - Movie name    -    Seats left - Price - Showing time")
    for i in range(len(movie_list)):
        print(f"{i+1:3}  {(movie_list[i].get_name()):30} {(movie_list[i].get_seats()):3} {(movie_list[i].get_price()):10} {(print_time(movie_list[i].get_time())):10} {((movie_list[i].get_position())):3}")
    
            
# allow the user to chose the theater
theater, theater_id = theater_choser()


# Function to update movies' names and seats
def update_movie():
    print("What movie would you like to update?")
    display_all_table()
    
    # allow the user to select a movie
    selected_movie = printed_movies[error_checker(0, len(movie_list), "int") - 1] 
    print("You have chosen", movie_list[selected_movie].get_name())

    # ask what the users wants to change
    print("Would you like to change its name (1) or update the price (2) or update the viewing time (3)?")
    selected_edit = error_checker(1, 3, "int")
    # change the movie's name
    if selected_edit == 1:
        # loop until the user inputs a name they are happy with 
        while True:
            new_name = input("What would you like to change the name to?")
            print(f"Are you sure you would like to change {movie_list[selected_movie].get_name()} to {new_name}? (type 1 for yes, 2 for no)")
            confirm = input()
            # change the movie name and exit the function
            if confirm == "1":
                movie_list[selected_movie].change_name(new_name)
                return
            # cancel the change and exit the function 
            elif confirm == "2":
                return
    # change the price of the movie
    elif selected_edit == 2:
        print(f"Currently there are {movie_list[selected_movie].get_seats()}, how many would you like to remove? (negative to add)")
        print("What is the price of the movie?")
        # find the price of the movie, 100,000 is the limit for greedy managers
        movie_price = error_checker(0,100000,"float")
        print(f"Are you sure that {{movie_list[selected_movie].get_name()}} will have a price of {movie_price}? (1 for yes, 2 for no, 3 to cancel addition)")
        # confirm the price and update the movie price if its correct
        confirm = input()
        if confirm == "1":
            movie_list[selected_movie].update_price()
            return
        # cancel the operation
        elif confirm == "3":
            return
    elif selected_edit == 3:

        print(f"What time would you like {movie_list[selected_movie].get_name()} to be shown at? (Enter time in 23:59 format)")
        minutes_after_midnight = error_checker(data_type="time")
        print(f"Are you sure that {movie_list[selected_movie].get_name()} will be shown at {print_time(minutes_after_midnight)}? (1 for yes, 2 for no, 3 to cancel addition)")
        confirm = input()
        if confirm == "1":
            movie_list[selected_movie].update_time()
        elif confirm == "3":
            return
        

        # run = True
        # while run:
        #     try:
        #         remove_seats = int(input())
        #         if movie_list[selected_movie].get_seats() - remove_seats > theater_cap[movie_list[selected_movie].get_theater_id() - 1][2]:
        #             print(f"{theater} is only able to hold {theater_cap[movie_list[selected_movie].get_theater_id() - 1][2]} seats, please add an amount of seats that would keep it below its limit")
        #         elif movie_list[selected_movie].get_seats() - remove_seats < 0:
        #             print(f"The maximum tickets this theater can sell is {movie_list[selected_movie].get_seats()}. Please enter a value that would not oversell the theater")
        #         else:
        #             run = False
        #             movie_list[selected_movie].decrease_seats(remove_seats)
        #             print(f"{movie_list[selected_movie].get_name()} currently has {movie_list[selected_movie].get_seats()} available seats")
        #     except ValueError:
        #         print("Please enter a valid integer")

    # elif selected_edit == 3:
    #     print(f"What time would you like {movie_list[selected_movie].get_name()} to be shown at? (Enter time in 23:59 format)")
    #     minutes_after_midnight = error_checker(data_type="time")
    #     print(f"Are you sure that {movie_list[selected_movie].get_name()} will be shown at {print_time(minutes_after_midnight)}? (1 for yes, 2 for no, 3 to cancel addition)")
    #     confirm = input()
    #     if confirm == "1":
    #         movie_list[selected_movie].change_time(minutes_after_midnight)
    #         return
    #     elif confirm == "3":
    #         return

# Function to delete movies from the movie list
def delete_movie():
    print("What movie would you like to delete? 0 to cancel")
    display_all_table()
    print_all()
    print(printed_movies)
    user_input = error_checker(0, len(movie_list), "int") - 1
    if user_input == -1:
        return
    selected_movie = printed_movies[user_input]
    print(selected_movie)
    print(printed_movies)
    
    
    

    print(f"Are you sure you would like to delete {movie_list[selected_movie].get_name()}? (type 1 for yes, 2 for no)")
    while True:
        confirm = input()
        if confirm in "1 yes Yes":
            print(f"{movie_list[selected_movie].get_name()} was deleted")
            movie_list[selected_movie].delete_movie_db()
            movie_list.pop(selected_movie)
            return 
        
        elif confirm in "2 no No":
            
            print(f"{movie_list[selected_movie].get_name()} has not been deleted")
            return
        else:
            print("Please enter either 1 (yes) or 2 (no)")

# Function to add a movie to the movie list
def add_movie():
    progress = 1
    run = True
    while run:
        if progress == 1:

            movie_name = input("What is the name of the movie?")
            print(f"Are you sure the movie is called {movie_name}? (1 for yes, 2 for no, 3 to cancel addition)")
            confirm = input()
            if confirm == "1":
                progress -= -1 
                
            elif confirm == "3":
                return
        if progress == 2:
            print("What is the price of the movie?")
            movie_price = error_checker(0,100000,"float")
            print(f"Are you sure that {movie_name} will have a price of {movie_price}? (1 for yes, 2 for no, 3 to cancel addition)")
            confirm = input()
            if confirm == "1":
                progress -=- 1
            elif confirm == "3":
                return
        if progress == 3:
            print(f"What time would you like {movie_name} to be shown at? (Enter time in 23:59 format)")
            minutes_after_midnight = error_checker(data_type="time")
            print(f"Are you sure that {movie_name} will be shown at {print_time(minutes_after_midnight)}? (1 for yes, 2 for no, 3 to cancel addition)")
            confirm = input()
            if confirm == "1":
                run = False
            elif confirm == "3":
                return

      

    # Generate the item in the class
    movie_id = movie_list[-1].get_id() + 1
    movie(movie_id, movie_name, theater_cap[theater_id-1][2], theater_cap[theater_id-1][1], theater_id, movie_price, minutes_after_midnight )
    movie_list[-1].add_movie()


def add_sale( ):

    display_all_table( )
    print("What movie would you like to create a sale for?")

    # selected_movie = error_checker(1, len(movie_list), "int") - 1
    # print((printed_movies))
    # print(error_checker(1, len(printed_movies), "int") -1 )
    # print(printed_movies[error_checker(1, len(printed_movies), "int") -1 ])
    # print(selected_movie)
    selected_movie = printed_movies[error_checker(0, len(movie_list), "int") - 1]
    # print(printed_movies)
    # print(selected_movie)
    print(movie_list[selected_movie].get_name())
    print(f"Currently there are {movie_list[selected_movie].get_seats()}, how many would you like to remove? (negative to add)")
    run = True
    while run:
        try:
            remove_seats = int(input())
            if movie_list[selected_movie].get_seats() - remove_seats > theater_cap[movie_list[selected_movie].get_theater_id() - 1][2]:
                print(f"{theater} is only able to hold {theater_cap[movie_list[selected_movie].get_theater_id() - 1][2]} seats, please add an amount of seats that would keep it below its limit")
            elif movie_list[selected_movie].get_seats() - remove_seats < 0:
                print(f"The maximum this movie can sell is {movie_list[selected_movie].get_seats()}. Please enter a value that would not oversell the theater")
            else:
                print(f"This will cost ${remove_seats*movie_list[selected_movie].get_price()}. Are you sure you would like to make this sale?(0 for no, 1 for yes, 2 to change seats)")
                confirm = input()
                if confirm == "1":
                    run = False
                    movie_list[selected_movie].decrease_seats(remove_seats)
                    print(f"{movie_list[selected_movie].get_name()} currently has {movie_list[selected_movie].get_seats()} available seats")
                elif confirm !="2":
                    return
                else:
                    print(f"Currently there are {movie_list[selected_movie].get_seats()}, how many would you like to remove? (negative to add)")
        except ValueError:
            print("Please enter a valid integer")
    

# Main run time organizer
# display_all_table()
while True:
    display_all_table()
    if len(printed_movies) == 0:
        print("This theater currently has no movies, please add some or change theaters")
        user_input = input("What would you like to run? \n1. Add a movie \n2. Change theater")
        if user_input == "1":
            add_movie()
        elif user_input == "2":
            theater, theater_id = theater_choser()
    else:
        
        user_input = input("What would you like to run? \n1. Display all the movies \n2. Update movie info \n3. Delete a movie \n4. Add a movie \n5. Add a sale \n6. Change theater")
        if user_input == "1":
            display_all_table()
        elif user_input == "2":
            update_movie()
        elif user_input == "3":
            delete_movie()
        elif user_input == "4":
            add_movie()
        elif user_input == "5":
            add_sale()
        elif user_input == "6":
            theater, theater_id = theater_choser()
        