''' This is a program which allows users to manage a movie database system with seats and save beyond the current session'''
# set up imports
import sqlite3

# Set up and connect to the database
DATABASE = "C:\\xampp3\htdocs\\2024-year-13-scol-classwork-OwenMenzies\\Python\\MovieManager.db"
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
        cursor.execute("UPDATE MovieIndex set MovieSeatsLeft = ? where MovieID == ?",(self._seats - quantity,self._id))
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
        
        cursor.execute("DELETE FROM MovieIndex WHERE MovieID = ?",(self._id,))
        connection.commit()

    # Add a movie to the database
    def add_movie(self):
     
        cursor.execute("INSERT INTO MovieIndex VALUES (?,?,?,?,?,?)",(self._id,self._name,self._seats,self._theater_id,self._movie_price,self._movie_time))
        connection.commit()

    # update time of database 
    def update_time(self,new_time):
        cursor.execute("UPDATE MovieIndex set MovieTime = ? where MovieID == ?",(new_time,self._id))
        connection.commit()
        self._movie_time = new_time

    # update price of database
    def update_price(self,new_price):
        cursor.execute("UPDATE MovieIndex set MoviePrice = ? where MovieID == ?",(new_price,self._id))
        connection.commit()
        self._movie_price = new_price
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
            # if the user inputs a non integer, print an error
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
            try:
                # split into hours and minutes
                hours,minutes = input().split(":")
                hours = int(hours)
                minutes = int(minutes)
             
                # check if time follows universal principles e.g. no 11:67 am
                if hours >= 0 and hours <24 and minutes >=0 and minutes <=59:
                    return hours*60+minutes
            
                else:
                    print("Please enter a valid time") 
            except ValueError:
                print("Please enter a valid time") 
   
            
# allow the user to chose a theater to log in to
def theater_choser():
        while True:
            print(f"Which theater would you like to log in to? (1 for Hi Vis Jacket (80 seats), 2 for Ladder and Clipboard (120 seats), 3 for Long Trenchcoat (200 seats))")
           
            # receive the input from the user and asign it to the desired theater
            theater_id = error_checker(1, 3, "int") - 1
            theater = theater_cap[theater_id][1]

            # confirm with user if the chosen theater is correct
            while True:
                print(f"Are you sure you would like to log in to {theater}? (1 to confirm, 2 to cancel)")
                confirm = input()
                if confirm == "1":
                    return theater, theater_id+1
                elif confirm == "2":
                    break

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


            
# allow the user to chose the theater
theater, theater_id = theater_choser()


# Function to update movies' names and seats
def update_movie():
    print("What movie would you like to update?")
    display_all_table()
    
    # allow the user to select a movie
    selected_movie = printed_movies[error_checker(1, len(printed_movies), "int") - 1] 
    print("You have chosen", movie_list[selected_movie].get_name())

    # ask_user what the users wants to change
    print("Would you like to change its name (1) or update the price (2) or update the viewing time (3)?")
    selected_edit = error_checker(1, 3, "int")
    # change the movie's name
    user_updating_movie = True

    while user_updating_movie == True:
        if selected_edit == 1:
            # loop until the user inputs a name they are happy with 
            while True:
                new_name = input("What would you like to change the name to?")
                ask_user = True
                if new_name == "" or new_name.isspace() == True:
                    print("Please enter a non whitespace name (" ")")
                    continue
                while ask_user:
                    print(f"Are you sure you would like to change {movie_list[selected_movie].get_name()} to {new_name}? (1 to confirm, 2 to change name, 3 to cancel)")
                    confirm = input()
                  
                    # change the movie name and exit the function
                    if confirm == "1":
                        movie_list[selected_movie].change_name(new_name)
                        return
                    elif confirm == "2":
                        ask_user = False
                    # cancel the change and exit the function 
                    elif confirm == "3":
                        return
                    else: 
                        print("Please enter either 1,2 or 3")
        # change the price of the movie
        elif selected_edit == 2:
            print("What is the new price of the movie?")
            # find the price of the movie, 100,000 is the limit for greedy managers
            movie_price = error_checker(0,100000,"float")
            # confirm the price and update the movie price if its correct
            ask_user = True
            while ask_user == True:
                print(f"Are you sure that {movie_list[selected_movie].get_name()} will have a price of {movie_price:.2f}? (1 to confirm, 2 to change price, 3 to cancel)")

                confirm = input()
                if confirm == "1":
                    movie_list[selected_movie].update_price(movie_price)
                    return
                elif confirm == "2":
                    ask_user = False
                # cancel the operation
                elif confirm == "3":
                    return
                else: 
                    print("Please enter either 1,2 or 3")
        # change the viewing time of the movie
        elif selected_edit == 3:

            print(f"What time would you like {movie_list[selected_movie].get_name()} to be shown at? (Enter time in 23:59 format)")
            minutes_after_midnight = error_checker(data_type="time")

            # check if the user inputs the correct time, and if so, update the database
            ask_user_user = True
            while ask_user_user == True:
                print(f"Are you sure that {movie_list[selected_movie].get_name()} will be shown at {print_time(minutes_after_midnight)}? (1 to confirm, 2 to change time, 3 to cancel addition)")
                confirm = input()
                if confirm == "1":
                    movie_list[selected_movie].update_time(minutes_after_midnight)
                    return
                if confirm == "2":
                    ask_user_user = False
                elif confirm == "3":
                    return
                else: 
                    print("Please enter either 1,2 or 3")
        


# Function to delete movies from the movie list
def delete_movie():
    
    display_all_table()
    print("What movie would you like to delete? 0 to cancel")
    user_input = error_checker(0, len(printed_movies), "int") - 1
    # cancel the function if the user inputs 0 (0 - 1 = -1)
    if user_input == -1:
        return
    selected_movie = printed_movies[user_input]
    
    
    
    # confirm the user wants to delete the chosen movie
    using_deleting_movie = True
    while using_deleting_movie == True:
        print(f"Are you sure you would like to delete {movie_list[selected_movie].get_name()}? (1 to confirm, 2 to change the movie, 3 to cancel deletion)")
        confirm = input()
        # delete the movie
        if confirm in "1 yes Yes":
            print(f"{movie_list[selected_movie].get_name()} was deleted")
            movie_list[selected_movie].delete_movie_db()
            movie_list.pop(selected_movie)
            
            using_deleting_movie = False 
            
        # inform the user that the movie was not deleted and return to main program manager
        elif confirm in "3":
            
            print(f"{movie_list[selected_movie].get_name()} has not been deleted")
            return
        # allow the user to select a different movie
        elif confirm == "2":
            print("What movie would you like to delete? 0 to cancel")
            display_all_table()
            user_input = error_checker(0, len(printed_movies), "int") - 1
            # cancel the function if the user inputs 0 (0 - 1 = -1)
            if user_input == -1:
                return
            selected_movie = printed_movies[user_input]
        else:
            print("Please enter either 1,2 or 3")
       

# Function to add a movie to the movie list
def add_movie():
    progress = 1
    # run until the user has successfully added a movie
    run = True
    while run:
        # check if the user is on the first step of adding the movie, add the movie's name
        if progress == 1:
            
            movie_name = input("What is the name of the movie?")
            if movie_name == "" or movie_name.isspace() == True:
                print("Please enter a non whitespace name (" ")")
                continue
            # confirm if the movie name is correct
            ask_user = True
            while ask_user:
                print(f"Are you sure the movie is called {movie_name}? (1 to confirm, 2 to change name, 3 to cancel addition)")
                confirm = input()
                # either advance the user, reask_user the quesiton, or end the program depending on what the user inputs
                if confirm == "1":
                    progress +=1
                    ask_user = False
                elif confirm == "2":
                    ask_user = False
                elif confirm == "3":
                    return
        # add the movie time
        if progress == 2:
            # create the movie price
            print("What is the price of the movie?")
            movie_price = error_checker(0,100000,"float")
            # confirm if the movie price is correct
            ask_user = True
            while ask_user == True:
                print(f"Are you sure that {movie_name} will have a price of {movie_price:.2f}? (1 to confirm, 2 to change the price, 3 to cancel addition)")
                
                confirm = input()
                # either advance the user, reask_user the quesiton, or end the program depending on what the user inputs

                if confirm == "1":
                    progress +=1
                    ask_user = False
                elif confirm == "2":
                    ask_user = False
                elif confirm == "3":
                    return
        # add the movie's showing time
        if progress == 3:
            
            print(f"What time would you like {movie_name} to be shown at? (Enter time in 23:59 format)")
            
            minutes_after_midnight = error_checker(data_type="time")

            # confirm if the movie time is correct
            ask_user = True
            while ask_user == True:
                print(f"Are you sure that {movie_name} will be shown at {print_time(minutes_after_midnight)}? (1 to confirm, 2 to change the time, 3 to cancel addition)")
                # either advance the user, reask_user the quesiton, or end the program depending on what the user inputs
                confirm = input()
                if confirm == "1":
                    run = False
                    ask_user = False
                elif confirm == "2":
                    ask_user = False
                elif confirm == "3":
                    return

      

    # Generate the item in the class, if there are no movies, set the movie_id to 1, else make it the largest id +1
    if len(movie_list) == 0:
        movie_id = 1
    else:
        movie_id = movie_list[-1].get_id() + 1
    # create the movie as an object
    movie(movie_id, movie_name, theater_cap[theater_id-1][2], theater_cap[theater_id-1][1], theater_id, movie_price, minutes_after_midnight )
    # add the movie to the database
    movie_list[-1].add_movie()

# add a sale for a movie
def add_sale( ):

    display_all_table( )
    print("What movie would you like to create a sale for?")


    selected_movie = printed_movies[error_checker(0, len(printed_movies), "int") - 1]
    # determine how many seats the user wants to sell or refund
    print(movie_list[selected_movie].get_name())
    print(f"Currently there are {movie_list[selected_movie].get_seats()}, how many seats would you like to remove? (negative to add)")
    # run until the user enters and confirms a valid quantity of seats
    run = True
    while run:
        try:
            
            remove_seats = int(input())
            # check if the user is trying to refund more seats than the theater has sold 
            if movie_list[selected_movie].get_seats() - remove_seats > theater_cap[movie_list[selected_movie].get_theater_id() - 1][2]:
                print(f"{theater} is only able to hold {theater_cap[movie_list[selected_movie].get_theater_id() - 1][2]} seats, please add an amount of seats that would keep the theater below its limit")
            # check if the user can input an amount that does not put the seats sold above the maximum capacity of the theater (overbooking)
            elif movie_list[selected_movie].get_seats() - remove_seats < 0:
                print(f"The maximum this movie can sell is {movie_list[selected_movie].get_seats()}. Please enter a value that would not oversell the theater")
            # allow the sale/refund and get confirmation
            else:
                if remove_seats < 0:
                    print(f"This will refund ${-1*remove_seats*movie_list[selected_movie].get_price()}. Are you sure you would like to make this refund? (1 to confirm, 2 to change quantity of seats, 3 to cancel)")
                else: 
                    print(f"This will cost ${remove_seats*movie_list[selected_movie].get_price()}. Are you sure you would like to make this sale? (1 to confirm, 2 to change quantity of seats, 3 to cancel)")
                # receive confirmation and either change the amount of seats or rerun the function or return to main run time function 
                run2 = True
                while run2:

                    confirm = input()
                    # execute seats edit
                    if confirm == "1":
                        run = False
                        run2 = False
                        movie_list[selected_movie].decrease_seats(remove_seats)
                        print(f"{movie_list[selected_movie].get_name()} currently has {movie_list[selected_movie].get_seats()} available seats")
                    # cancel addition
                    elif confirm =="3":
                        return
                    # change seats
                    elif confirm == "2":
                        run2 = False
                        print(f"Currently there are {movie_list[selected_movie].get_seats()}, how many would you like to remove? (negative to add)")
                    else:
                        print("Please enter either 1,2 or 3")
        except ValueError:
            print("Please enter a valid integer")
    

# Main run time organizer
# display_all_table()
while True:
    display_all_table()
    # check if there is aren't any movies in the theater, and if so, limit the user to adding movies or changing theaters
    if len(printed_movies) == 0:
        print("This theater currently has no movies, please add some or change theaters")
        user_input = input("What would you like to run? \n1. Add a movie \n2. Change theater ")
        
        # allow the user to select the prefered option 
        if user_input == "1":
            add_movie()
        elif user_input == "2":
            theater, theater_id = theater_choser()
    # allow the user to select the prefered option 
    else:
        
        user_input = input("What would you like to run? \n1. Update movie info \n2. Delete a movie \n3. Add a movie \n4. Add a sale \n5. Change theater ")
      
        if user_input == "1":
            update_movie()
        elif user_input == "2":
            delete_movie()
        elif user_input == "3":
            add_movie()
        elif user_input == "4":
            add_sale()
        elif user_input == "5":
            theater, theater_id = theater_choser()
        