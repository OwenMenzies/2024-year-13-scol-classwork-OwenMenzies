''' This is a program which allows users to manage a movie database system with seats and save beyond the current session'''
# setup imports
import sqlite3
# set up and connect to database
DATABASE = 'MovieManager.db'
connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()
movieList = []
# create the class of movie
query = "SELECT TheaterID, TheaterName, TheaterSeats FROM Theater ORDER BY TheaterID"
cursor.execute(query)
theaterCap = []
results = cursor.fetchall() 

for i in results:
    theaterCap.append([i[0],i[1],i[2]])
    

class movie ():
    # initize the class 
    def __init__ (self,MovieID,MovieName,MovieSeatsLeft,TheaterName,TheaterID):
        self._id = MovieID
        self._name = MovieName
        self._seats = MovieSeatsLeft
        self._theater = TheaterName
        self._theaterId = TheaterID
        movieList.append(self)
    
    
    # return the individual items
    def getName(self):
        return self._name
    def getId(self):
        return self._id
    def getSeats(self):
        return self._seats
    def getTheater(self):
        return self._theater
    def getTheaterId(self):
        return self._theaterId


# execute setup query
query = "SELECT MovieID,MovieName,MovieSeatsLeft,TheaterName ,Theater.TheaterID FROM MovieIndex INNER JOIN Theater ON MovieIndex.MovieTheaterID = Theater.TheaterID"
cursor.execute(query)

results = cursor.fetchall()
for result in results:
   
    movie(result[0],result[1],result[2],result[3],result[4])
    test = [result[0],result[1],result[2],result[3],result[4]]

def errorChecker(lower,upper,type):
    
    while True:
        if type == "int":
            try:
                value = int(input())
                if value >= lower and value <= upper:
                    return value
                else:
                    print("Please enter an integer between",lower,"and",upper)
            except ValueError:
                print("Please enter an integer between",lower,"and",upper)


# display the specific movie
def displayInfo(self):
        print("MovieID:", self.getID())
        print("MovieName:",self.getName())
        print("MovieSeatsLeft:",self.getSeats())
        print("TheaterName:",self.getTheater())
    
def displayAllTable():
    print("Movie number - MovieName    -    MovieSeatesLeft - TheaterName")
    for i in range(len(movieList)):
        print(f"{i+1:3}  {(movieList[i].getName()):30} {(movieList[i].getSeats()):3}      {movieList[i].getTheater():20}")

#display all movies     
def displayAll():
    for i in movieList:
        displayInfo(i)

# display the movies in a neat fashion

def updateMovie():
    print("What movie would you like to update?")
    for i in range(len(movieList)):
        
        print(f" {str(i+1):2} {movieList[i].getName():30} {movieList[i].getSeats():3}")


    selectedMovie = errorChecker(1,len(movieList), "int") -1
    print("You have chosen",movieList[selectedMovie].getName())

    print("Would you like to change its name (1) or update the amount of seats (2)?")
    
    selectedEdit = errorChecker(1,2, "int")
    
    if selectedEdit == 1:
        
        run = True
        while run == True:
            
            newName = input("What would you like to change the name to?")
            print("Are you sure you would like to change",movieList[selectedMovie].getName(),"to",newName+"? (type 1 for yes, 2 for no)")
            confirm = input()
            
            if confirm == "1":
                run = False
                movieList[selectedMovie].changeName(newName)
            
            elif confirm == "2":
                run = False

    elif selectedEdit ==2:
        print("Currently there are " + str(movieList[selectedMovie].getSeats()),"how many would you like to remove? (negative to add)")
        
        run = True
        while run == True:
            try:
                     
                removeSeats = int(input())
            
                if movieList[selectedMovie].getSeats() - removeSeats > theaterCap[movieList[selectedMovie].getTheaterId()-1][2]:
                    print(movieList[selectedMovie].getTheater(),"is only able to hold",theaterCap[movieList[selectedMovie].getTheaterId()-1][2],
                          "seats, please add a amount of seats that would keep it below its limit")
                
                elif movieList[selectedMovie].getSeats() - removeSeats <0:

                    print("The maximum this movie can sell is",str(movieList[selectedMovie].getSeats())+". Please enter a value that would not oversell the theater")
               
                else:
                    run = False
                    movieList[selectedMovie].decreaseSeats(removeSeats)
                    print(movieList[selectedMovie].getName(),"currently has",movieList[selectedMovie].getSeats(),"avalible seats")
           
            except ValueError:
                print("Please enter a valid integer")
        
   

# imediately display the entire table 
displayAllTable()

     
            


# main run time organiser
while True:
    userInput = input("What would you like to run? \n1. Display all the movies \n2. Update seats \n3. Delete a movie \n4. Add a movie \n5.  ")
    if userInput == "1":
        displayAllTable()
    elif userInput == "2":
        updateMovie()
    # elif userInput == "3":
    #     deleteMovie()
    # elif userInput == "4":
    #     addMovie()
    # elif userInput == "5":
    #     pass