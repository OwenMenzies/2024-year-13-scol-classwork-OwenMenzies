# class Teacher():
#     def __init__(self,studentClass):
#         self._class = studentClass


class Student():
    def __init__(self, name,age):
        self._name = name  
        self._age = age
        studentList.append(self)
    def displayInfo(self):
        print(self._name,"is",self._age,"years old")

    def get_name(self):
        return self._name
    def get_age(self):
        return self._age


def printNames():
    for student in studentList:
        print(student.get_name(),"", end = "")



studentList = []
Student("Jack",16)
Student("and",17)
Student("Jill",18)
Student("went",19)
Student("up",20)
Student("a",21)
Student("hill",22)
Student("to",23)
Student("fetch",24)
Student("a",25)
Student("pale",26)
Student("of",27)
Student("water.",28)
Student("I",29)
Student("Don't",30)
Student("know",26)
Student("what",26)
Student("they",26)
Student("did",26)
Student("up",26)
Student("there",26)
Student("but",26)
Student("they",26)
Student("came",26)
Student("back",26)
Student("with",26)
Student("a",26)
Student("daughter",26)
studentList[2].displayInfo()
print(studentList)
print("hi")

printNames()
