import mysql.connector as MS
import datetime
import os
from Person import Person
from Course import Course
from dotenv import load_dotenv
class Database(object):
    def selectUniqueCompany(self):
        statement='SELECT DISTINCT(company) from Person;'
        db1 = MS.connect(host="localhost",user=os.getenv('USER'),passwd=os.getenv("PASSWORD"),database=os.getenv('DATABASE'))
        cursor = db1.cursor()
        cursor.execute(statement)
        temp = cursor.fetchall()
        final=[]
        for x in temp:
            final.append(x[0])
        return final
    def selectUniqueCourse(self):
        statement='SELECT DISTINCT(courseName) from Course;'
        db1 = MS.connect(host="localhost",user=os.getenv('USER'),passwd=os.getenv("PASSWORD"),database=os.getenv('DATABASE'))
        cursor = db1.cursor()
        cursor.execute(statement)
        temp = cursor.fetchall()
        final=[]
        for x in temp:
            final.append(x[0])
        return final
    def selectPerson(self,fName,initial,lName,company,course):
        insertAnd=False
        pStatement=''
        data=()
        if company!='':
            pStatement='Select ID,firstName,MiddleInitial,LastName,Company from Person WHERE INSTR(firstName,%s) and INSTR(middleInitial,%s) AND INSTR(LastName,%s) AND Company=%s;'
            data=(fName,initial,lName,company)
        else:
            pStatement='Select ID,firstName,MiddleInitial,LastName,Company from Person WHERE INSTR(firstName,%s) and INSTR(middleInitial,%s) AND INSTR(LastName,%s);'
            data=(fName,initial,lName)
        db1 = MS.connect(host="localhost",user=os.getenv('USER'),passwd=os.getenv("PASSWORD"),database=os.getenv('DATABASE'))
        cursor = db1.cursor()
        cursor.execute(pStatement,data)

        
        personList=cursor.fetchall()
        personList=list(personList)
        courseList=[]
        for row in personList:
            statement='Select id, courseName, DateTaken, Expiry,Instructor from Course, Person_has_Course Where '+ str(row[0])+' = Person_has_Course.Person_ID AND course.ID=Person_has_Course.Course_ID'
            if course!=None and course!='':
                statement=statement+" AND courseName = '"+course+"';"
            else:
                statement=statement+';'

            cursor.execute(statement)
            tCourses=cursor.fetchall()
            tDone=[]
            
            for c in tCourses:
                tempCourse=Course(c[0],c[1],c[2],c[3],c[4])
                tDone.append(tempCourse)

            courseList.append(tDone)

        if course!=None and course!='':
            i=0
            while(i<len(personList)):
                if not courseList[i]:
                    personList.pop(i)
                    courseList.pop(i)
                    i=i-1
                i=i+1
        db1.close()
        rpList=[]

        i=0
        for p in personList:
            tempPerson = Person(p[0],p[1],p[2],p[3],p[4],courseList[i])
            rpList.append(tempPerson)
            i=i+1

        return rpList

    def selectPersonById(self,idIn):
        pStatement='Select ID,firstName,MiddleInitial,LastName,Company from Person WHERE ID='+str(idIn)+';'
        db1 = MS.connect(host="localhost",user=os.getenv('USER'),passwd=os.getenv("PASSWORD"),database=os.getenv('DATABASE'))
        cursor = db1.cursor()
        cursor.execute(pStatement)

        temp=cursor.fetchall()
        p=list(temp)[0]
        cStatement='Select id, courseName, DateTaken, Expiry,Instructor from Course, Person_has_Course Where '+ str(p[0])+' = Person_has_Course.Person_ID AND course.ID=Person_has_Course.Course_ID'
        cursor.execute(cStatement)
        cList=cursor.fetchall()
        courseList=[]
        for c in cList:
            tempCourse=Course(c[0],c[1],c[2],c[3],c[4])
            courseList.append(tempCourse)
        person = Person(p[0],p[1],p[2],p[3],p[4],courseList)
        return person

    def insertPerson(self,firstName,middleInitial,lastName,company):
        load_dotenv()

        statement=(
        "INSERT INTO Person(FirstName,MiddleInitial,LastName,Company)"
        "VALUES (%s,%s,%s,%s);"
        )
        data = (firstName,middleInitial,lastName,company)
        db1 = MS.connect(host="localhost",user=os.getenv('USER'),passwd=os.getenv("PASSWORD"),database=os.getenv('DATABASE'))
        cursor = db1.cursor()
        cursor.execute(statement,data)
        db1.commit()
        statement2=(
        "SELECT LAST_INSERT_ID();"
        )
        cursor.execute(statement2)
        a=cursor.fetchall()
        db1.close()
        return(a[0][0])
#expiry of 1900-01-01 will be handled as does not expire
    def insertCourse(self,CourseName,DateTaken,Expiry,Instructor):
        try:
            load_dotenv()
            statement=(
            "INSERT INTO Course(courseName,DateTaken,Expiry,Instructor)"
            "VALUES (%s,%s,%s,%s)"
            )
            data = (CourseName,DateTaken,Expiry,Instructor)
            db1 = MS.connect(host="localhost",user=os.getenv('USER'),passwd=os.getenv("PASSWORD"),database=os.getenv('DATABASE'))
            cursor = db1.cursor()
            cursor.execute(statement,data)

            db1.commit()
            db1.close()
        except Exception as e:

            raise
    def highestId(self):
        load_dotenv()
        statement=(
        "select id from person"
        )
        db1 = MS.connect(host="localhost",user=os.getenv('USER'),passwd=os.getenv("PASSWORD"),database=os.getenv('DATABASE'))
        cursor = db1.cursor()
        cursor.execute(statement)
        temp = cursor.fetchall()
        highest=0
        for x in temp:
            if x[0]>highest:
                highest=x[0]
        return highest
    def updatePerson(self,id,first,initial,last,company):
        load_dotenv()
        statement=('UPDATE Person SET FirstName=%s,MiddleInitial=%s,LastName=%s,Company=%s WHERE ID=%s')
        data=(first,initial,last,company,id)
        db1 = MS.connect(host="localhost",user=os.getenv('USER'),passwd=os.getenv("PASSWORD"),database=os.getenv('DATABASE'))
        cursor = db1.cursor()
        cursor.execute(statement,data)
        db1.commit()
        db1.close()
    def selectCourse(self,CourseName,DateTaken,Expiry,Instructor):
        load_dotenv()
        statement=(
        "SELECT * FROM Course WHERE INSTR(courseName,%s) AND INSTR(DateTaken,%s) AND INSTR(Expiry,%s) AND INSTR(Instructor,%s)"
        )
        data = (CourseName,DateTaken,Expiry,Instructor)
        db1 = MS.connect(host="localhost",user=os.getenv('USER'),passwd=os.getenv("PASSWORD"),database=os.getenv('DATABASE'))
        cursor = db1.cursor()
        cursor.execute(statement,data)
        temp = cursor.fetchall()
        cList=[]
        for c in temp:
            cTemp = Course(c[0],c[1],c[2],c[3],c[4])
            cList.append(cTemp)
        db1.commit()
        db1.close()

        return cList
    def insertM2M(self,PersonID,CourseID):
        load_dotenv()

        try:
            statement=(
            "INSERT INTO Person_has_Course(Person_ID,Course_ID)"
            "VALUES (%s,%s)"
            )
            data=(PersonID,CourseID)
            db1 = MS.connect(host="localhost",user=os.getenv('USER'),passwd=os.getenv("PASSWORD"),database=os.getenv('DATABASE'))
            cursor = db1.cursor()
            cursor.execute(statement,data)
            db1.commit()
            db1.close()
            return 0
        except Exception as e:
            print(e)


            return 1
    def deleteM2M(self,PersonID,CourseID):
        try:
            statement=(
            "DELETE FROM Person_has_Course WHERE Person_ID=%s AND Course_ID=%s;"
            )

            data=(PersonID,CourseID)
            db1 = MS.connect(host="localhost",user=os.getenv('USER'),passwd=os.getenv("PASSWORD"),database=os.getenv('DATABASE'))
            cursor = db1.cursor()
            cursor.execute(statement,data)
            db1.commit()
            db1.close()
            return 0
        except Exception as e:
            print(e)
            return 1
    def deletePerson(self,PersonID):
        try:
            statement=(
            "DELETE FROM Person WHERE ID=%s;"
            )
            data=[PersonID]
            db1 = MS.connect(host="localhost",user=os.getenv('USER'),passwd=os.getenv("PASSWORD"),database=os.getenv('DATABASE'))
            cursor = db1.cursor()
            cursor.execute(statement,data)
            db1.commit()
            db1.close()
            return 0
        except Exception as e:
            print("DeletePerson:")
            print(e)
            return 1
    def __init__(self):
        load_dotenv()
        db1 = MS.connect(host="localhost",user=os.getenv('USER'),passwd=os.getenv("PASSWORD"))
        print("Connecting to database: "+os.getenv('DATABASE'))
        cursor = db1.cursor()
        #create database if it does not exist
        try:
            sql = str('CREATE DATABASE '+os.getenv('DATABASE'))
            cursor.execute(sql)
        except:
            print('Database already exists, continuing')

        db1 = MS.connect(host="localhost",user=os.getenv('USER'),passwd=os.getenv("PASSWORD"),database=os.getenv('DATABASE'))
        cursor = db1.cursor()
        #create Person table if it does not exist
        sql ="CREATE TABLE IF NOT EXISTS Person (ID INT NOT NULL AUTO_INCREMENT,FirstName VARCHAR(45) NOT NULL,MiddleInitial VARCHAR(1) NULL,LastName VARCHAR(45) NOT NULL,Company VARCHAR(100) NOT NULL,PRIMARY KEY (ID),UNIQUE INDEX ID_UNIQUE (ID ASC) VISIBLE);"
        cursor.execute(sql)
        db1.commit()
        #create course table if not exists
        sql = "CREATE TABLE IF NOT EXISTS Course ( ID INT NOT NULL AUTO_INCREMENT, courseName VARCHAR(100) NOT NULL,DateTaken DATE NOT NULL,Expiry DATE NULL,Instructor VARCHAR(100) NOT NULL,PRIMARY KEY (ID),UNIQUE INDEX ID_UNIQUE (ID ASC) VISIBLE);"
        cursor.execute(sql)
        db1.commit()


        sql = "CREATE TABLE IF NOT EXISTS Person_has_Course (  Person_ID INT NOT NULL,  Course_ID INT NOT NULL,  PRIMARY KEY (Person_ID, Course_ID),  INDEX fk_Person_has_Course_Course1_idx (Course_ID ASC) VISIBLE,  INDEX fk_Person_has_Course_Person_idx (Person_ID ASC) VISIBLE,  CONSTRAINT fk_Person_has_Course_Person    FOREIGN KEY (Person_ID)    REFERENCES Person (ID)    ON DELETE NO ACTION    ON UPDATE NO ACTION,  CONSTRAINT fk_Person_has_Course_Course1    FOREIGN KEY (Course_ID)    REFERENCES Course (ID)    ON DELETE NO ACTION    ON UPDATE NO ACTION);"
        cursor.execute(sql)
        db1.commit()

        
        db1.close()
