from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Person import Person
from Course import Course
from Database import Database
import qdarkgraystyle

#pyinstaller C:\Users\Christian\Desktop\Work\CourseContainer.py --onefile
class QPersonWidget(QWidget):
    def __init__(self,person):
        super(QPersonWidget,self).__init__()
        self.person = person
        self.layout = QHBoxLayout()
        vlay= QVBoxLayout()
        self.info = QLabel(str(person))
        courses=''
        for c in person.courseList:
            cLabel=QLabel(str(c))
            cLabel.setMinimumHeight(40)
            vlay.addWidget(cLabel)
            courses=courses+str(c)
        
        self.courses=QLabel(courses)
        self.layout.addWidget(self.info)
        self.layout.addLayout(vlay)
        self.setLayout(self.layout)
class QCourseWidget(QWidget):
    def __init__(self,course):
        super(QCourseWidget,self).__init__()
        self.course = course
        self.layout= QHBoxLayout()
        self.layout.addWidget(QLabel(str(course)))
        self.setLayout(self.layout)

class NewPersonAddCourseWidget(QWidget):
    def closeEvent(self, event):
        t=NewPersonWidget()
        for w in windowList:
            if type(w) ==type(NewPersonAddCourseWidget()):
                windowList.remove(w)
                return
    def __init__(self):
        def addcListItem(list,c):
            t = QCourseWidget(c)
            myQListWidgetItem = QListWidgetItem(list)
            myQListWidgetItem.setSizeHint(t.sizeHint())
            list.addItem(myQListWidgetItem)
            list.setItemWidget(myQListWidgetItem, t)

        def submit_clicked():
            global addCoursesToPeopleList
            addCoursesToPeopleList=[]
            for x in list.selectedItems():
                addCoursesToPeopleList.append(list.itemWidget(x).course)
            self.close()

        super().__init__()
        courses = db.selectCourse('','','','')
        masterLayout = QVBoxLayout()
        list = QListWidget()
        list.setSelectionMode(3)
        masterLayout.addWidget(list)
        submitButton=QPushButton("submit")
        submitButton.setToolTip("Submit selection of course")
        submitButton.clicked.connect(submit_clicked)
        masterLayout.addWidget(submitButton)
        self.setLayout(masterLayout)

        for c in courses:
            addcListItem(list,c)
class NewPersonWidget(QWidget):
    list
    def closeEvent(self, event):
            for w in windowList:
                if type(w) ==type(NewPersonWidget()):
                    windowList.remove(w)
                    return
    def __init__(self):
        def updateCourses():
            courseList.clear()
            for c in addCoursesToPeopleList:
                t = QCourseWidget(c)
                myQListWidgetItem = QListWidgetItem(courseList)
                myQListWidgetItem.setSizeHint(t.sizeHint())
                courseList.addItem(myQListWidgetItem)
                courseList.setItemWidget(myQListWidgetItem, t)
            self.update()

        def add_clicked():
            p=Person(0,firstNameLine.text(),middleInitialLine.text(),lastNameLine.text(),companyLine.text(),[])
            t=QPersonWidget(p)
            myQListWidgetItem = QListWidgetItem(list)
            myQListWidgetItem.setSizeHint(t.sizeHint())
            list.addItem(myQListWidgetItem)
            list.setItemWidget(myQListWidgetItem, t)
            firstNameLine.clear()
            middleInitialLine.clear()
            lastNameLine.clear()
            companyLine.clear()

        def remove_clicked():
            for x in list.selectedItems():
                list.takeItem(list.row(x))
            updateCourses()
        def add_course_clicked():
            global windowList
            for w in windowList:
                if type(w) ==type(NewPersonAddCourseWidget()):
                    w.activateWindow()
                    return
            window=NewPersonAddCourseWidget()
            window.setMinimumSize(500,300)
            window.setWindowTitle("Course Manager - Add Person - Attach Course")
            window.show()
            windowList.append(window)

        def submit_clicked():
            global addCoursesToPeopleList
            db = Database()

            while(list.count()>0):
                list.setCurrentRow(0)
                p=list.itemWidget(list.currentItem()).person
                id=db.insertPerson(p.fName,p.initial,p.lName,p.company)
                for c in addCoursesToPeopleList:
                    db.insertM2M(id,c.id)
                list.takeItem(0)
            self.close()
        
        def company_item_clicked():
            companyLine.clear()
            companyLine.insert(companyList.currentItem().text())
        
        super().__init__()
        
        masterLayout=QHBoxLayout()
        leftLayout = QVBoxLayout()
        topLayout = QGridLayout()
        midLayout= QHBoxLayout()
        midRightLayout = QVBoxLayout()
        midFarRightLayout = QVBoxLayout()
        bottomLayout= QVBoxLayout()
        firstNameLabel = QLabel('First Name')
        firstNameLine = QLineEdit()
        topLayout.addWidget(firstNameLine,1,0)
        topLayout.addWidget(firstNameLabel,0,0)

        middleInitialLabel = QLabel('Initial')
        middleInitialLine = QLineEdit()
        middleInitialLine.setMaxLength(1)
        topLayout.addWidget(middleInitialLine,1,1)
        topLayout.addWidget(middleInitialLabel,0,1)

        lastNameLabel = QLabel('Last Name')
        lastNameLine = QLineEdit()
        topLayout.addWidget(lastNameLine,1,2)
        topLayout.addWidget(lastNameLabel,0,2)

        companyLabel = QLabel('Company')
        companyLine = QLineEdit()
        topLayout.addWidget(companyLine,1,3)
        topLayout.addWidget(companyLabel,0,3)

        addButton = QPushButton("add")
        addButton.setToolTip("Add person")
        addButton.setMaximumWidth(100)
        addButton.setMinimumWidth(100)
        addButton.clicked.connect(add_clicked)
        topLayout.addWidget(addButton,1,4)

        list = QListWidget()
        list.setSelectionMode(3)
        midLayout.addWidget(list)

        removeButton=QPushButton("remove")
        removeButton.setToolTip("Remove selected people")
        removeButton.clicked.connect(remove_clicked)
        midRightLayout.addWidget(removeButton)

        addCourseButton=QPushButton("add course")
        addCourseButton.setToolTip("Add course to all new people")
        addCourseButton.clicked.connect(add_course_clicked)

        midRightLayout.addWidget(addCourseButton)
        midRightLayout.setAlignment(Qt.AlignTop)

        companyList=QListWidget()
        companyList.itemClicked.connect(company_item_clicked)
        db=Database()
        cList=db.selectUniqueCompany()
        for x in cList:
            companyList.addItem(x)

        companyListLabel = QLabel("Company List")
        companyList.setMaximumWidth(100)
        midRightLayout.addWidget(companyListLabel)
        midRightLayout.addWidget(companyList)

        addedCoursesLabel = QLabel("Selected Courses")
        refFont=QFont()
        refFont.setBold(True)
        refreshButton = QPushButton('⟳')
        refreshButton.setFont(refFont)
        refreshButton.setToolTip("Refresh")
        refreshButton.setMinimumWidth(25)
        refreshButton.setMaximumWidth(25)
        refreshButton.clicked.connect(updateCourses)
        topRightLayout=QHBoxLayout()
        topRightLayout.addWidget(addedCoursesLabel)
        topRightLayout.addWidget(refreshButton)
        midFarRightLayout.addLayout(topRightLayout)
        courseList=QListWidget()
        courseList.setMinimumWidth(275)
        courseList.setMaximumWidth(275)
        midFarRightLayout.addWidget(courseList)
        
        midLayout.addLayout(midRightLayout)
        submitButton=QPushButton("submit")
        submitButton.setToolTip("Submit list of persons to database")
        submitButton.clicked.connect(submit_clicked)
        bottomLayout.addWidget(submitButton)


        leftLayout.addLayout(topLayout)
        leftLayout.addLayout(midLayout)
        leftLayout.addLayout(bottomLayout)
        masterLayout.addLayout(leftLayout)
        masterLayout.addLayout(midFarRightLayout)
        self.setLayout(masterLayout)

class EditWidget(QWidget):
    def __init__(self,idIn):
        def update_clicked():
            if firstNameLine.text()!="":
                firstNameLabel.setText(firstNameLine.text())
            if middleInitialLine.text()!="":
                middleInitialLabel.setText(middleInitialLine.text())
            if lastNameLine.text()!="":
                lastNameLabel.setText(lastNameLine.text())
            if companyLine.text()!="":
                companyLabel.setText(companyLine.text())
            firstNameLine.setText('')
            middleInitialLine.setText('')
            lastNameLine.setText('')
            companyLine.setText('')

        def remove_clicked():
            if len(assignedCoursesList.selectedItems())<1:
                return
            c=assignedCoursesList.itemWidget(assignedCoursesList.selectedItems()[0]).course
            assignedCoursesList.takeItem(assignedCoursesList.currentRow())
            t = QCourseWidget(c)
            myQListWidgetItem = QListWidgetItem(allCourseList)
            myQListWidgetItem.setSizeHint(t.sizeHint())
            allCourseList.addItem(myQListWidgetItem)
            allCourseList.setItemWidget(myQListWidgetItem, t)
            if c in finalAddList:
                finalAddList.remove(c)
            else:
                finalRemoveList.append(c)
            
        def add_clicked():
            if len(allCourseList.selectedItems())<1:
                return
            c=allCourseList.itemWidget(allCourseList.selectedItems()[0]).course
            allCourseList.takeItem(allCourseList.currentRow())
            t = QCourseWidget(c)
            myQListWidgetItem = QListWidgetItem(assignedCoursesList)
            myQListWidgetItem.setSizeHint(t.sizeHint())
            assignedCoursesList.addItem(myQListWidgetItem)
            assignedCoursesList.setItemWidget(myQListWidgetItem, t)
            if c in finalRemoveList:
                finalRemoveList.remove(c)
            else:
                finalAddList.append(c)

        def submit_clicked():
            db=Database()
            db.updatePerson(id,firstNameLabel.text(),middleInitialLabel.text(),lastNameLabel.text(),companyLabel.text())
            for x in finalAddList:
                db.insertM2M(id,x.id)
            for x in finalRemoveList:
                db.deleteM2M(id,x.id)
            self.close()

        finalAddList=[]
        finalRemoveList=[]
        id=idIn
        super().__init__()
        masterLayout = QVBoxLayout()
        topLayout=QGridLayout()
        midLayout=QHBoxLayout()
        midLeftLayout=QVBoxLayout()
        midCenterLayout=QVBoxLayout()
        midRightLayout=QVBoxLayout()
        bottomLayout=QHBoxLayout()
        db=Database()
        p=db.selectPersonById(id)
        #top
        idLabel=QLabel(str(id))
        topLayout.addWidget(idLabel,0,0)
        firstNameLabel=QLabel(p.fName)
        topLayout.addWidget(firstNameLabel,0,1)

        middleInitialLabel=QLabel(p.initial)
        topLayout.addWidget(middleInitialLabel,0,2)

        lastNameLabel=QLabel(p.lName)
        topLayout.addWidget(lastNameLabel,0,3)

        companyLabel=QLabel(p.company)
        topLayout.addWidget(companyLabel,0,4)

        firstNameLine=QLineEdit()
        topLayout.addWidget(firstNameLine,1,1)

        middleInitialLine=QLineEdit()
        middleInitialLine.setMaxLength(1)
        topLayout.addWidget(middleInitialLine,1,2)

        lastNameLine=QLineEdit()
        topLayout.addWidget(lastNameLine,1,3)

        companyLine=QLineEdit()
        topLayout.addWidget(companyLine,1,4)

        updateButton=QPushButton("update")
        updateButton.setToolTip("Update the name to the current fields")
        updateButton.clicked.connect(update_clicked)
        topLayout.addWidget(updateButton,1,5)

        #Middle
        assignedCoursesLabel=QLabel("Assigned Courses")
        midLeftLayout.addWidget(assignedCoursesLabel)

        assignedCoursesList=QListWidget()
        for c in p.courseList:
            t = QCourseWidget(c)
            myQListWidgetItem = QListWidgetItem(assignedCoursesList)
            myQListWidgetItem.setSizeHint(t.sizeHint())
            assignedCoursesList.addItem(myQListWidgetItem)
            assignedCoursesList.setItemWidget(myQListWidgetItem, t)
        midLeftLayout.addWidget(assignedCoursesList)

        addButton=QPushButton("<<")
        addButton.setToolTip("Assign course to person")
        addButton.clicked.connect(add_clicked)
        midCenterLayout.addWidget(addButton)

        removeButton=QPushButton(">>")
        removeButton.setToolTip("Remove course from person")
        removeButton.clicked.connect(remove_clicked)
        midCenterLayout.addWidget(removeButton)

        allCoursesLabel=QLabel("All Courses")
        midRightLayout.addWidget(allCoursesLabel)
        tempCourseList=db.selectCourse("","",'','')
        tempPersonCoursesList=p.courseList
        #O(n^2) could be better
        removeList=[]
        for x in tempCourseList:
            for y in tempPersonCoursesList:
                if x.id==y.id:
                    removeList.append(x)
                    break
        for x in removeList:
            tempCourseList.remove(x)
        allCourseList=QListWidget()
        for c in tempCourseList:
            t = QCourseWidget(c)
            myQListWidgetItem = QListWidgetItem(allCourseList)
            myQListWidgetItem.setSizeHint(t.sizeHint())
            allCourseList.addItem(myQListWidgetItem)
            allCourseList.setItemWidget(myQListWidgetItem, t)
        midRightLayout.addWidget(allCourseList)

        midLayout.addLayout(midLeftLayout)
        midLayout.addLayout(midCenterLayout)
        midLayout.addLayout(midRightLayout)
        #bottom
        submitButton=QPushButton("Submit")
        submitButton.setToolTip("Submit updates to database")
        submitButton.clicked.connect(submit_clicked)
        bottomLayout.addWidget(submitButton)

        masterLayout.addLayout(topLayout)
        masterLayout.addLayout(midLayout)
        masterLayout.addLayout(bottomLayout)

        self.setLayout(masterLayout)

class NewCourseWidget(QWidget):
    list
    def closeEvent(self, event):
            for w in windowList:
                if type(w) ==type(NewCourseWidget()):
                    windowList.remove(w)
                    return
    def __init__(self):
        def add_clicked():
            c=Course(0,NameLine.text(),dateTakenLine.text(),expiryLine.text(),instructorLine.text())
            t=QCourseWidget(c)
            myQListWidgetItem = QListWidgetItem(list)
            myQListWidgetItem.setSizeHint(t.sizeHint())
            list.addItem(myQListWidgetItem)
            list.setItemWidget(myQListWidgetItem, t)
            NameLine.clear()
            dateTakenLine.clear()
            expiryLine.clear()
            instructorLine.clear()
        def remove_clicked():
            for x in list.selectedItems():
                list.takeItem(list.row(x))
        def submit_clicked():
            db = Database()
            while(list.count()>0):
                list.setCurrentRow(0)
                c=list.itemWidget(list.currentItem()).course
                try:
                    id=db.insertCourse(c.name,c.dateTaken,c.expiry,c.instructor)
                except Exception as e:
                    errorWindow = QWidget()
                    errorWindow.setWindowTitle("Error")
                    windowList.append(errorWindow)
                    eVbox= QVBoxLayout()
                    eLabel=QLabel("Error adding 1 or many courses\nThis is most likely due to a bad date or empty field, dates should be in the format YYYY-MM-DD")
                    eLabel2=QLabel(str(e)+"\nYou may close this window")
                    eVbox.addWidget(eLabel)
                    eVbox.addWidget(eLabel2)
                    errorWindow.setLayout(eVbox)
                    errorWindow.show()
                list.takeItem(0)
            self.close()
        super().__init__()
        masterLayout = QVBoxLayout()
        topLayout = QGridLayout()
        midLayout= QHBoxLayout()
        midRightLayout = QVBoxLayout()
        bottomLayout= QVBoxLayout()
        NameLabel = QLabel('Name')
        NameLine = QLineEdit()
        topLayout.addWidget(NameLine,1,0)
        topLayout.addWidget(NameLabel,0,0)

        dateTakenLabel = QLabel('Date Taken')
        dateTakenLine = QLineEdit()
        topLayout.addWidget(dateTakenLine,1,1)
        topLayout.addWidget(dateTakenLabel,0,1)

        expiryLabel = QLabel('Expiry (Leave blank for no expiry)')
        expiryLine = QLineEdit()
        topLayout.addWidget(expiryLine,1,2)
        topLayout.addWidget(expiryLabel,0,2)

        instructorLabel = QLabel('Instructor')
        instructorLine = QLineEdit()
        topLayout.addWidget(instructorLine,1,3)
        topLayout.addWidget(instructorLabel,0,3)

        addButton = QPushButton("add")
        addButton.setToolTip("Add course")
        addButton.clicked.connect(add_clicked)
        topLayout.addWidget(addButton,1,4)

        list = QListWidget()
        list.setSelectionMode(3)
        midLayout.addWidget(list)

        removeButton=QPushButton("remove")
        removeButton.setToolTip("Remove selected courses")
        removeButton.clicked.connect(remove_clicked)

        midRightLayout.addWidget(removeButton)
        midRightLayout.setAlignment(Qt.AlignTop)
        midLayout.addLayout(midRightLayout)

        submitButton=QPushButton("submit")
        submitButton.setToolTip("Submit list of persons to database")
        submitButton.clicked.connect(submit_clicked)
        bottomLayout.addWidget(submitButton)


        masterLayout.addLayout(topLayout)
        masterLayout.addLayout(midLayout)
        masterLayout.addLayout(bottomLayout)
        self.setLayout(masterLayout)
        masterLayout.addWidget(submitButton)
        self.setLayout(masterLayout)

global addCoursesToPeopleList
addCoursesToPeopleList=[]
global windowList
windowList=[]
app = QApplication([])
window = QWidget()
window.setMinimumSize(800,600)
db=Database()

#layouts
masterLayout = QVBoxLayout()
topLayout = QGridLayout()
midLayout= QHBoxLayout()
midRightLayout = QVBoxLayout()
bottomLayout = QHBoxLayout()
bottomLeftLayout = QHBoxLayout()
bottomRightLayout = QHBoxLayout()

#slots
def addListItem(p):

    t = QPersonWidget(p)
    myQListWidgetItem = QListWidgetItem(list)
    myQListWidgetItem.setSizeHint(t.sizeHint())
    list.addItem(myQListWidgetItem)
    list.setItemWidget(myQListWidgetItem, t)
def search_clicked():
    list.clear()
    pList = db.selectPerson(firstNameLine.text(),middleInitialLine.text(),lastNameLine.text(),companyBox.currentText(),courseBox.currentText())
    for p in pList:
        addListItem(p)
    firstNameLine.clear()
    middleInitialLine.clear()
    lastNameLine.clear()
    refresh_clicked()
    infoLabel.setText("Search complete")
def add_person_clicked():
    global windowList
    for window in windowList:
        if type(window) ==type(NewPersonWidget()):
            window.activateWindow()
            return
    w=NewPersonWidget()
    w.setWindowTitle("Course Manager - Add Person")
    w.setMinimumSize(500,350)
    w.show()
    windowList.append(w)
    infoLabel.setText("")
def add_course_clicked():
    global windowList
    for window in windowList:
        if type(window) ==type(NewCourseWidget()):
            window.activateWindow()
            return
    w=NewCourseWidget()
    w.setWindowTitle("Course Manager - Add Course")
    w.setMinimumSize(500,350)
    w.show()
    windowList.append(w)
    infoLabel.setText("")
def refresh_clicked():
    companyBox.clear()
    companyList = db.selectUniqueCompany()
    companyBox.addItem('')
    for x in companyList:
        companyBox.addItem(x)
    courseBox.clear()
    courseList=db.selectUniqueCourse()
    courseBox.addItem('')
    for x in courseList:
        courseBox.addItem(x)
    infoLabel.setText("Refreshed dropdowns")
def remove_clicked():
    removeButton.setEnabled(False)
    unlockCheck.setCheckState(0)
    if len(list.selectedItems())!=1:
        return
    p=list.itemWidget(list.currentItem()).person
    db = Database()
    for c in p.courseList:
        db.deleteM2M(p.id,c.id)
    db.deletePerson(p.id)
    infoLabel.setText("Successfully removed person")
def edit_clicked():
    #current
    global windowList
    if len(list.selectedItems())>1:
        infoLabel.setText("You can only have 1 person selected to edit")
        return
    elif len(list.selectedItems())<1:
        infoLabel.setText("You must have 1 person selected to edit")
        return
    w=EditWidget(list.itemWidget(list.selectedItems()[0]).person.id)
    w.setWindowTitle("Edit "+str(list.itemWidget(list.selectedItems()[0]).person.name))
    w.setMinimumSize(800,600)
    w.show()
    windowList.append(w)
def toggle_remove():
    if unlockCheck.isChecked():
        removeButton.setEnabled(True)
    else:
        removeButton.setEnabled(False)
#widgets
#top layer widgets
firstNameLabel = QLabel('First Name')
firstNameLine = QLineEdit()
topLayout.addWidget(firstNameLine,1,0)
topLayout.addWidget(firstNameLabel,0,0)

middleInitialLabel = QLabel('Initial')
middleInitialLine = QLineEdit()
middleInitialLine.setMaxLength(1)

topLayout.addWidget(middleInitialLine,1,1)
topLayout.addWidget(middleInitialLabel,0,1)

lastNameLabel = QLabel('Last Name')
lastNameLine = QLineEdit()
topLayout.addWidget(lastNameLine,1,2)
topLayout.addWidget(lastNameLabel,0,2)

companyLabel = QLabel('Company')
companyBox = QComboBox()
companyBox.setMinimumWidth(120)
companyBox.setMaximumWidth(150)
companyList = db.selectUniqueCompany()
companyBox.addItem('')
for x in companyList:
    companyBox.addItem(x)
topLayout.addWidget(companyBox,1,3)
topLayout.addWidget(companyLabel,0,3)

courseLabel = QLabel('Course')
courseBox = QComboBox()
courseBox.setMinimumWidth(120)
courseBox.setMaximumWidth(150)
courseList = db.selectUniqueCourse()
courseBox.addItem('')
for x in courseList:
    courseBox.addItem(x)
topLayout.addWidget(courseBox,1,4)
topLayout.addWidget(courseLabel,0,4)
refFont=QFont()
refFont.setBold(True)
refreshButton = QPushButton('⟳')
refreshButton.setFont(refFont)
refreshButton.setToolTip("Refresh")
refreshButton.setMinimumWidth(25)
refreshButton.setMaximumWidth(25)
refreshButton.clicked.connect(refresh_clicked)
topLayout.addWidget(refreshButton,1,5)
searchButton = QPushButton('search')
searchButton.setToolTip('Search with the given parameters')
searchButton.setMinimumWidth(60)
searchButton.clicked.connect(search_clicked)
topLayout.addWidget(searchButton,1,6)

#mid layer widgets
list = QListWidget()
list.setSelectionMode(3)
midLayout.addWidget(list)
unlockCheck=QCheckBox("unlock remove")
unlockCheck.setToolTip("Unlock the remove button")
unlockCheck.stateChanged.connect(toggle_remove)

removeButton = QPushButton('remove')
removeButton.setToolTip("Remove the selected person from database")
removeButton.setMinimumWidth(95)
removeButton.setMaximumWidth(95)
removeButton.setEnabled(False)
removeButton.clicked.connect(remove_clicked)
editButton = QPushButton('edit')
editButton.setToolTip("Edit the selected person's entry")
editButton.setMinimumWidth(95)
editButton.setMaximumWidth(95)
editButton.clicked.connect(edit_clicked)
newPersonButton = QPushButton('add new people')
newPersonButton.clicked.connect(add_person_clicked)
newPersonButton.setToolTip('Create new entries')
newPersonButton.setMinimumWidth(95)
newPersonButton.setMaximumWidth(95)


midRightLayout.addWidget(unlockCheck)
midRightLayout.addWidget(removeButton)
midRightLayout.addWidget(editButton)
midRightLayout.addWidget(newPersonButton)
midRightLayout.setAlignment(Qt.AlignBottom)
midLayout.addLayout(midRightLayout)

#bottom layer widgets
exportButton = QPushButton("export to JSON")
exportButton.setMaximumWidth(160)
exportButton.setToolTip('Export search results to JSON file')
exportButton.setEnabled(False)
bottomLeftLayout.addWidget(exportButton)
infoLabel=QLabel("")
bottomLeftLayout.addWidget(infoLabel)

newCourseButton = QPushButton("add new courses")
newCourseButton.setToolTip("Create new courses")
newCourseButton.setMinimumWidth(95)
newCourseButton.setMaximumWidth(95)
newCourseButton.clicked.connect(add_course_clicked)
bottomRightLayout.addWidget(newCourseButton)

bottomRightLayout.setAlignment(Qt.AlignRight)
bottomLayout.addLayout(bottomLeftLayout)
bottomLayout.addLayout(bottomRightLayout)

masterLayout.addLayout(topLayout)
masterLayout.addLayout(midLayout)
masterLayout.addLayout(bottomLayout)
window.setLayout(masterLayout)
window.setWindowTitle("Course Manager")
window.show()
app.setStyleSheet(qdarkgraystyle.load_stylesheet())
app.exec()
