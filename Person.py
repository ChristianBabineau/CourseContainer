class Person(object):


    def __init__(self,Id, First,Initial,Last,Company,CourseList):
        self.id=Id
        self.fName=First
        self.initial=Initial
        self.lName=Last
        self.name=str(First)+" "+str(Initial)+" "+ str(Last)
        self.company = Company
        if CourseList==None:
            self.courseList=[]
        else:
            self.courseList=CourseList

    def __str__(self):
        if(self.id==0):
            return f"{self.name}, {self.company}"
        else:
            return f"id: {self.id} , {self.name}, {self.company}"

    def addCourse(self,items):
        if type(items)==type(1):
            self.courseList.append(items)
            self.courseList=list(set(self.courseList))
            print("Successfully added item to: "+self.name)
            return
        elif type(items)==type([]):
            for item in items:
                self.courseList.append(item)
            self.courseList=list(set(self.courseList))
            print("Successfully added items to: "+self.name)
            return
        else:
            print('Error: could not add items')
            return
