from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from datetime import date
import os

global userid,  pnameValue, pdateValue

def Chat(request):
    if request.method == 'GET':
       return render(request, 'Chat.html', {})

def searchQuery(query, data):
    arr = data.split(" ")
    qry = query.split(" ")
    count =0
    for i in range(len(qry)):
        for j in range(len(arr)):
            if qry[i] == arr[j]:
                count = count + 1
    return count

def getTime(doctor):
    available = "Not Available, Not Available, Not Available"
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'HospitalDB',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select * FROM timetable1")
        rows = cur.fetchall()
        for row in rows:
            if row[0] == doctor:
                available = row[0]+","+row[1]+","+row[2]
                break
    return available

def ChatData(request):
    if request.method == 'GET':
        query = request.GET.get('mytext', False)
        desc = "Unable to recognize your query"
        score = 0
        doctor = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'HospitalDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,speciality FROM adddoctor")
            rows = cur.fetchall()
            for row in rows:
                description = row[1]
                count = searchQuery(query.lower(), description.lower())
                if count > score:
                    score = count
                    desc = description
                    doctor = row[0]
        details = getTime(doctor).split(",")            
        output = "Doctor Name: "+details[0]+"\r\nAvailability Date: "+details[1]+"\r\nAvailability Slot Timing: "+details[2]            
        return HttpResponse(output, content_type="text/plain")    
    

def ViewAppointments(request):
    if request.method == 'GET':
        global userid
        output = ""
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'HospitalDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM online_appointments")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size="" color="black">'+str(row[0])+'</td>'
                output+='<td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+str(row[2])+'</td>'                
        context= {'data':output}
        return render(request, 'ViewAppointments.html', context)

def ViewMeetings(request):
    if request.method == 'GET':
        global userid
        output = ""
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'HospitalDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM meetings")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size="" color="black">'+str(row[0])+'</td>'
                output+='<td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+str(row[2])+'</td>'                
        context= {'data':output}
        return render(request, 'ViewMeetings.html', context)

def ViewTimeTable(request):
    if request.method == 'GET':
        global userid
        output = ""
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'HospitalDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM timetable1")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size="" color="black">'+str(row[0])+'</td>'
                output+='<td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+str(row[2])+'</td>'                
        context= {'data':output}
        return render(request, 'ViewTimeTable.html', context)

def ViewPatientPrescription(request):
    if request.method == 'GET':
        global userid
        output = ""
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'HospitalDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM addpatient where patient_id='"+userid+"'")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size="" color="black">'+str(row[0])+'</td>'
                output+='<td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+str(row[2])+'</td>'
                output+='<td><font size="" color="black">'+str(row[3])+'</td>'
                output+='<td><font size="" color="black">'+str(row[4])+'</td>'
                output+='<td><font size="" color="black">'+str(row[5])+'</td>'
                output+='<td><font size="" color="black">'+str(row[6])+'</td>'
                output+='<td><font size="" color="black">'+str(row[7])+'</td>'
        context= {'data':output}
        return render(request, 'ViewPatientPrescription.html', context)        

def Prescription(request):
    if request.method == 'GET':
        global pnameValue, pdateValue
        global userid
        pnameValue = request.GET['pname']
        pdateValue = request.GET['pdate']
        context= {'data':"Patient Name: "+pnameValue}
        return render(request, 'Prescription.html', context)

def PrescriptionAction(request):
    global pnameValue, pdateValue, userid
    prescription = request.POST.get('t1', False)
    db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'HospitalDB',charset='utf8')
    db_cursor = db_connection.cursor()
    student_sql_query = "update addpatient set prescription='"+prescription+"' where visit_date='"+pdateValue+"' and patient_id='"+pnameValue+"' and prescription='Pending'"
    db_cursor.execute(student_sql_query)
    db_connection.commit()
    print(db_cursor.rowcount, "Record Inserted")
    if db_cursor.rowcount == 1:
        context= {'data':'Prescription generated successfully for patient '+pnameValue}
        return render(request, 'Doctorscreen.html', context)
    else:
        context= {'data':'Error in generating prescription'}
        return render(request, 'DoctorScreen.html', context)

def ViewPatientReport(request):
    if request.method == 'GET':
        global userid
        output = ""
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'HospitalDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM addpatient where consult_doctor='"+userid+"'")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size="" color="black">'+str(row[0])+'</td>'
                output+='<td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+str(row[2])+'</td>'
                output+='<td><font size="" color="black">'+str(row[3])+'</td>'
                output+='<td><font size="" color="black">'+str(row[4])+'</td>'
                output+='<td><font size="" color="black">'+str(row[5])+'</td>'
                if row[6] != 'Pending':
                    output+='<td><font size="" color="black">'+str(row[6])+'</td>'
                else:
                    output+='<td><a href=\'Prescription?pname='+str(row[0])+'&pdate='+str(row[7])+'\'><font size=3 color=black>Click Here</font></a></td>'
                output+='<td><font size="" color="black">'+str(row[7])+'</td>'
        context= {'data':output}
        return render(request, 'ViewPatientReport.html', context)        

def ViewPrescription(request):
    if request.method == 'GET':
        output = ""
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'HospitalDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM addpatient")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size="" color="black">'+str(row[0])+'</td>'
                output+='<td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+str(row[2])+'</td>'
                output+='<td><font size="" color="black">'+str(row[3])+'</td>'
                output+='<td><font size="" color="black">'+str(row[4])+'</td>'
                output+='<td><font size="" color="black">'+str(row[5])+'</td>'
                output+='<td><font size="" color="black">'+str(row[6])+'</td>'
                output+='<td><font size="" color="black">'+str(row[7])+'</td>'                
        context= {'data':output}
        return render(request, 'ViewPrescription.html', context)      


def ViewHospitalDetails(request):
    if request.method == 'GET':
        output = ""
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'HospitalDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM adddoctor")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size="" color="black">'+str(row[0])+'</td>'
                output+='<td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+str(row[2])+'</td>'
                output+='<td><font size="" color="black">'+str(row[3])+'</td>'
                output+='<td><font size="" color="black">'+str(row[4])+'</td>'
                output+='<td><font size="" color="black">'+str(row[5])+'</td>'
                output+='<td><font size="" color="black">'+str(row[6])+'</td>'
                output+='<td><font size="" color="black">'+str(row[7])+'</td>'
                output+='<td><font size="" color="black">'+str(row[8])+'</td>'
        context= {'data':output}
        return render(request, 'ViewHospitalDetails.html', context)

def OnlineAppointmentsAction(request):
    if request.method == 'POST':
        global userid
        available_date = request.POST.get('t1', False)
        slot = request.POST.get('t2', False)
        
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'HospitalDB',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO online_appointments(sername,online_date,available_slots) VALUES('"+str(userid)+"','"+available_date+"','"+slot+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            context= {'data':'Online Appointments time updated'}
            return render(request, 'OnlineAppointments.html', context)
        else:
            context= {'data':'Error in updating Online Appointments details'}
            return render(request, 'OnlineAppointments.html', context)

def OnlineAppointments(request):
    if request.method == 'GET':
       return render(request, 'OnlineAppointments.html', {})   

def ScheduleMeetingsAction(request):
    if request.method == 'POST':
        global userid
        available_date = request.POST.get('t1', False)
        slot = request.POST.get('t2', False)
        
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'HospitalDB',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO meetings(username,meeting_date,available_slots) VALUES('"+str(userid)+"','"+available_date+"','"+slot+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            context= {'data':'Meetings time updated'}
            return render(request, 'ScheduleMeetings.html', context)
        else:
            context= {'data':'Error in updating meeting details'}
            return render(request, 'ScheduleMeetings.html', context)

def ScheduleMeetings(request):
    if request.method == 'GET':
       return render(request, 'ScheduleMeetings.html', {})    

def UpdateTimeTableAction(request):
    if request.method == 'POST':
        global userid
        available_date = request.POST.get('t1', False)
        slot = request.POST.get('t2', False)
        
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'HospitalDB',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO timetable1(username,time_table,available_slots) VALUES('"+str(userid)+"','"+available_date+"','"+slot+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            context= {'data':'Time table updated'}
            return render(request, 'UpdateTimeTable.html', context)
        else:
            context= {'data':'Error in updating timetable details'}
            return render(request, 'UpdateTimeTable.html', context)

def UpdateTimeTable(request):
    if request.method == 'GET':
       return render(request, 'UpdateTimeTable.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def ViewInsurance(request):
    if request.method == 'GET':
       return render(request, 'ViewInsurance.html', {})    

def PatientLogin(request):
    if request.method == 'GET':
       return render(request, 'PatientLogin.html', {})    

def DoctorLogin(request):
    if request.method == 'GET':
       return render(request, 'DoctorLogin.html', {})

def PatientSignup(request):
    if request.method == 'GET':
        output = '<tr><td><font size="" color="black">Choose&nbsp;Doctor</b></td><td><select name="t5">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'HospitalDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM adddoctor")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+row[0]+'">'+row[0]+'</option>'
        output +="</select></td></tr>"
        context= {'data':output}
        return render(request, 'PatientSignup.html', context)
        

def AddDoctor(request):
    if request.method == 'GET':
       return render(request, 'AddDoctor.html', {})

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})

def AdminLoginAction(request):
    if request.method == 'POST':
        global userid
        user = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if user == "admin" and password == "admin":
            context= {'data':'Welcome '+user}
            return render(request, 'AdminScreen.html', context)
        else:
            context= {'data':'Invalid Login'}
            return render(request, 'AdminLogin.html', context)

def PatientSignupAction(request):
    if request.method == 'POST':
        today = date.today()
        disease = request.POST.get('t1', False)
        age = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        fee = request.POST.get('t4', False)
        doctor = request.POST.get('t5', False)
        pid = request.POST.get('t6', False)
        if pid == "0":
            con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'HospitalDB',charset='utf8')
            with con:
                cur = con.cursor()
                cur.execute("select count(*) from addpatient")
                rows = cur.fetchall()
                for row in rows:
                    pid = row[0] + 1
                    break
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'HospitalDB',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO addpatient(patient_id,disease_description,age,contact_no,fee_paid,consult_doctor,prescription,visit_date) VALUES('"+str(pid)+"','"+disease+"','"+age+"','"+contact+"','"+fee+"','"+doctor+"','Pending','"+str(today)+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            context= {'data':'IN_Patient details added with Patient ID = '+str(pid)}
            return render(request, 'PatientSignup.html', context)
        else:
            context= {'data':'Error in adding patient details'}
            return render(request, 'PatientSignup.html', context)


def PatientLoginAction(request):
    if request.method == 'POST':
        global userid
        pid = request.POST.get('t1', False)
        status = 'none'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'HospitalDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select patient_id FROM addpatient")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == int(pid):
                    userid = pid
                    status = 'success'
                    break
        if status == 'success':
            output = 'Welcome '+pid
            context= {'data':output}
            return render(request, 'PatientScreen.html', context)
        else:
            context= {'data':'Invalid Patient ID'}
            return render(request, 'PatientLogin.html', context)

def AddDoctorAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        email = request.POST.get('t3', False)
        contact = request.POST.get('t4', False)
        qualification = request.POST.get('t5', False)
        experience = request.POST.get('t6', False)
        hospital = request.POST.get('t7', False)
        address = request.POST.get('t8', False)
        speciality = request.POST.get('t9', False)
        output = 'none'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'HospitalDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM adddoctor")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username+" Username already exists"                    
        if output == "none":
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'HospitalDB',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO adddoctor(username,password,emailid,contact_no,qualification,experience_details,hospital_name,address,speciality) VALUES('"+username+"','"+password+"','"+email+"','"+contact+"','"+qualification+"','"+experience+"','"+hospital+"','"+address+"','"+speciality+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                context= {'data':'Doctor details added'}
                return render(request, 'AddDoctor.html', context)
            else:
                context= {'data':'Error in adding doctor details'}
                return render(request, 'AddDoctor.html', context)
        else:
            context= {'data':output}
            return render(request, 'AddDoctor.html', context)  


def DoctorLoginAction(request):
    if request.method == 'POST':
        global userid, hospital
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        status = 'none'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'HospitalDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,password FROM adddoctor")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and row[1] == password:
                    userid = username
                    status = 'success'
                    break
        if status == 'success':
            output = 'Welcome '+username
            context= {'data':output}
            return render(request, 'DoctorScreen.html', context)
        else:
            context= {'data':'Invalid username'}
            return render(request, 'DoctorLogin.html', context)




        
    
