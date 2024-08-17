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


# imediately display the entire table 
displayAllTable()

     
            


# main run time organiser
while True:
    userInput = input("What would you like to run? \n1. Display all the movies \n2. Update seats \n3. Delete a movie \n4. Add a movie \n5.  ")
    if userInput == "1":
        displayAllTable()
    # elif userInput == "2":
    #     updateMovie()
    # elif userInput == "3":
    #     deleteMovie()
    # elif userInput == "4":
    #     addMovie()
    # elif userInput == "5":
    #     pass