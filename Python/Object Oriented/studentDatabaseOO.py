classList = []
class Student():
    # initilize the student 
    def __init__ (self,name,age,phone,classes):
        self._name = name
        self._age = age
        self._phone = phone
        self._enrolled = True
        self._classes = classes
        studentList.append(self)

    # return all the information of the student
    def getInfo(self):
        return [self._name,self._age,self._phone,self._enrolled,self._classes]
    
    def getAll(self):
        print ("Name:", self._name, "\nAge: ",self._age,"\nPhone:", self._phone,"\nClasses:")
        for i in self._classes:
            print(i,end = " ")

    def getName(self):
        return self._name
    def getAge(self):
        return self._age
    def getClasses(self):
        return self._classes
    def getEnroled(self):
        return self._enrolled
    def getPhone(self):
        return self._phone
    
  
    # change the info to the new info
    def setInfo(self,name,age,phone,classes,enrolled = True):
        self._name = name
        self._age = age
        self._phone = phone
        self._enrolled = enrolled
        self._classes = classes
  
def displayInfo(self):
    print("Name:", self._name)
    print("Age:",self._age)
    print("Phone number:", self._phone)
    print("Enrolled:",self._enrolled)
    print("Classes: ",end = "")
    
    for i in self._classes:
        print(i,end = " ")
    print("")
       



def genStudents():

    import csv
    with open ('C:\\xampp3\\htdocs\\2024-year-13-scol-classwork-OwenMenzies\\Python\\Object Oriented\\studentcsv.csv', newline = '') as csvfile:
        fileReader = csv.reader(csvfile)
        for line in fileReader:
            classes = []
            for i in range(3,8):
                classes.append(line[i])
            Student(line[0], int(line[1]), int(line[2]), classes)

def classCounter(studentList,checkClass):
    number = 0
    studentsInClass = []
    for i in studentList:
        currentClasses = i.getClasses()
        for j in currentClasses:
            if j in checkClass:
                number+=1
                if i not in studentsInClass:
                    studentsInClass.append(i)
    if len(studentsInClass) == 0:
        return "No students are in this class"
    return len(studentsInClass),studentsInClass


def genClassList():
    
    for i in studentList:
        for j in i.getClasses():
            if j not in classList:
                classList.append(j)
    print(classList)

studentList = []
genStudents()
Student("Bob",12,1234567890,["ENG","MAT","PHY","ART","DIG"])
for i in studentList:
    print(i.getInfo())
# print(studentList[].getInfo())



# print the students which are a part of certain classes 
def classChecker ():
    for i in range(len(classList)):
        print(str(i) + ". ",classList[i])
    try:
        checkClass = int(input("Which class would you like to check? "))
    except ValueError:
        print("Please enter a number between 1 and", len(classList))
    try:
        num, students = classCounter(studentList,classList[checkClass])
    except:
        print("No students in this class")
        return 
    for i in students:
        i.getAll()

    print(num)

def studentChecker():
    counter = 0
    student = input("What student do you require the information for?")
    for i in studentList:
        if student in i.getName():
            displayInfo(i)
            counter += 1
    if counter != 0:
        print(counter,"result(s) found")
    else:
        print("No results found")
    
def ageChecker():
    printed = False
    age = int(input("What age would you like to search for?"))
    
    for i in studentList:
        if i.getAge() == age:
            displayInfo(i)
            printed = True

    if printed == False:
        print("No students were",age,"years old")

def studentDeleter():
    deadGuy = input("what student would you like to delete?")
    k = 0
    for i in range(len(studentList)):
        print(i)
        if deadGuy in studentList[i-k].getName():
            print("Are you sure you would like to delete", studentList[i-k].getName()+"? (1 to delete, 2 to not delete)")
            die = input()
            if die.lower() in ("yes die absolutely fuck yes yeah hell yeah kill him fuck him fuck you 1"):
                studentList.pop(i-k)
                k += 1
                print(k)

def nameUpper(name):
    newName = name[0].upper()
    for i in range(1,len(name)):
     newName += name[i]
    return newName
def studentAdder():
    name,age,phone,classes = input("Please enter the students name, age, phone number and classes seperated by a hyphen (-)").split("-")
    firstName, lastName = name.split(" ")
    firstName = nameUpper(firstName)
    lastName = nameUpper(lastName)
    age = int(age)
    phone = int(phone)
    classes = classes.upper
    classes = classes.split(" ")
    print(name,age,phone,classes)
   

genClassList()

while True:
    userInput = input("What would you like to run? \n1. check classes \n2. student info \n3. student age \n4. delete student \n5. add student ")
    if userInput == "1":
        classChecker()
    elif userInput == "2":
        studentChecker()
    elif userInput == "3":
        ageChecker()
    elif userInput == "4":
        studentDeleter()
    elif userInput == "5":
        studentAdder()
