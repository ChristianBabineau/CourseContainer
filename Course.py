import datetime
class Course(object):

    def __init__(self, Id,Name,DateTaken,Expiry,Instructor):
        self.id = Id
        self.name = Name
        self.dateTaken=DateTaken
        self.expiry=None
        if Expiry == '':
            self.expiry=datetime.date(1900,1,1)
        else:
            self.expiry=Expiry
        self.instructor=Instructor

    def __str__(self):
        if self.id==0 and self.expiry==datetime.date(1900,1,1):
            return f"{self.name}\n\ttaken: {self.dateTaken}\n\texpires: never \n\tinstructor: {self.instructor}"
        if self.id==0:
            return f"{self.name}\n\ttaken: {self.dateTaken}\n\texpires: {self.expiry} \n\tinstructor: {self.instructor}"
        if self.id!=0 and self.expiry==datetime.date(1900,1,1):
            return f"{self.name}, id: {self.id}\n\ttaken: {self.dateTaken}\texpires: never \n\tinstructor: {self.instructor}"
        return f"{self.name}, id: {self.id}\n\ttaken: {self.dateTaken}\texpires: {self.expiry} \n\tinstructor: {self.instructor}"
