import xlsxwriter
from Database import Database
import datetime
#✔
#pass in persons

def createSheet(dataIn,bookIn,sheetIn):
    db=Database()
    #find all unique courses and people
    personDict={}
    courseDict={}
    companyDict={}
    sortedDataIn=personSorter(dataIn)
    for p in sortedDataIn:
        personDict[str(p)]=p
    for p in personDict.values():
        companyDict[p.company]=1
        for c in p.courseList:
            courseDict[c.id]=[]
            courseDict[c.id].append(c.getNameAndExpo())
            courseDict[c.id].append(c.expiry)
    
    
    workbook=xlsxwriter.Workbook(bookIn+'.xlsx')
    wrap = workbook.add_format({'text_wrap': True,'align':'center','valign':'vcenter'})
    wrapOdd = workbook.add_format({'text_wrap': True,'align':'center','valign':'vcenter','bg_color':'#e0dede'})
    worksheet=workbook.add_worksheet(sheetIn)
    i=1
    for c in courseDict.values():
        worksheet.write(0,i,c[0],wrap)
        worksheet.set_column(i,i,max(len(c[0])-20,26))
        i=i+1
    
    i=1
    for p in personDict.values():
        if i%2==0:        
            worksheet.set_row(i,24,wrap)
        else:
            worksheet.set_row(i,24,wrapOdd)
        worksheet.write(i,0,p.name)
        for c in p.courseList:
            writable=''
            if courseDict[c.id][1]>=datetime.date.today()or courseDict[c.id][1]==datetime.date(1900,1,1):
                writable='✔'
            else:
                writable='EXP'
            if i%2==0:
                worksheet.write(i,list(courseDict.keys()).index(c.id)+1,writable)
            else:
                worksheet.write(i,list(courseDict.keys()).index(c.id)+1,writable)
        i=i+1
    worksheet.set_column_pixels(0,1000,144)
    if len(companyDict.keys())==1:
        companyFormat = workbook.add_format({'text_wrap': True,'align':'center','valign':'vcenter','bold':True,'font_size':16})
        if len(list(companyDict.keys())[0])*16>144:
            worksheet.set_column_pixels(0,0,len(list(companyDict.keys())[0])*14)
        worksheet.write(0,0,list(companyDict.keys())[0],companyFormat)
    worksheet.freeze_panes(1, 1)
    workbook.close()

def personSorter(peopleIn):
    returnList=[]
    placed=False
    for p in peopleIn:
        if not returnList:
            returnList.append(p)
        for x in returnList:
            if p.lName<x.lName:
                returnList.insert(returnList.index(x),p)
                placed=True
                break
        if not placed:
            returnList.append(p)
    return returnList
