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
    for p in dataIn:
        personDict[str(p)]=p
    for p in personDict.values():
        companyDict[p.company]=1
        for c in p.courseList:
            courseDict[c.id]=c.getNameAndExpo()
    
    
    workbook=xlsxwriter.Workbook(bookIn+'.xlsx')
    wrap = workbook.add_format({'text_wrap': True,'align':'center','valign':'vcenter'})
    wrapOdd = workbook.add_format({'text_wrap': True,'align':'center','valign':'vcenter','bg_color':'#e0dede'})
    worksheet=workbook.add_worksheet(sheetIn)
    i=1
    for c in courseDict.values():
        worksheet.write(0,i,c,wrap)
        i=i+1
    i=1
    for p in personDict.values():
        if i%2==0:        
            worksheet.set_row(i,24,wrap)
        else:
            worksheet.set_row(i,24,wrapOdd)
        worksheet.write(i,0,p.name)
        for c in p.courseList:
            if i%2==0:
                worksheet.write(i,list(courseDict.keys()).index(c.id)+1,'✔')
            else:
                worksheet.write(i,list(courseDict.keys()).index(c.id)+1,'✔')
        i=i+1
    worksheet.set_column_pixels(0,1000,144)
    if len(companyDict.keys())==1:
        companyFormat = workbook.add_format({'text_wrap': True,'align':'center','valign':'vcenter','bold':True,'font_size':16})
        if len(list(companyDict.keys())[0])*16>144:
            worksheet.set_column_pixels(0,0,len(list(companyDict.keys())[0])*14)
        worksheet.write(0,0,list(companyDict.keys())[0],companyFormat)
    workbook.close()
