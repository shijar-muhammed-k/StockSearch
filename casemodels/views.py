import json
import os

from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect, render

from . import models

cur = connection.cursor()

# Create your views here.


def index(request):
    cur.execute('''select * from CaseDetails;''')
    pics = cur.fetchall()
    data = []
    for i in pics:
        data.append([i[1], i[3], i[2]])
    return render(request, 'index.html', {'pic': reversed(data[-3:]), 'sample': reversed(data[-3:])})


def products(request):
    cur.execute('''select * from CaseDetails;''')
    pics = cur.fetchall()
    data = []
    for i in pics:
        data.append([i[1], i[3], i[2]])
    return render(request, 'Products.html', {'products': reversed(data)})


def searchCase(request, ctype):
    cur.execute('select * from DesignDetails where casename = "' + ctype + '";')
    pics = cur.fetchall()
    data = []
    for i in pics:
        data.append([i[1], i[3], i[2]])
    return render(request, 'SearchCase.html', {'products': reversed(data), 'type': ctype})


def searchDesign(request, ctype, dtype):
    cur.execute('select phonename, ' + dtype.lower().replace(" ", "") + ' from ' + ctype.lower().replace(" ", "") + ';')
    phones = cur.fetchall()
    cur.execute(
        'select DesignImage from DesignDetails where casename = "' + ctype + '"')
    design = cur.fetchone()
    phoneList = {}
    for i in phones:
        phoneList[i[0]] = i[1]

    phoneListJson = json.dumps(phoneList)
    return render(request, 'SearchStock.html', {'design': design[0], 'phoneStock': phoneListJson})


def login(request):
    flag = 0
    if request.method == 'POST':
        username = request.POST['userName']
        password = request.POST['password']
        if username == 'admin' and password == 'admin':
            return render(request, 'admin/AddCase.html')
        else:
            flag = 1
            return render(request, 'admin/login.html', {'flag': flag})
    else:
        return render(request, 'admin/login.html', {'flag': flag})


def logout(request):
    return render(request, 'index.html')


def addCase(request):
    cur.execute("select * from CaseDetails;")
    case = cur.fetchall()
    cases = []
    for i in case:
        cases.append(i[2])
    if request.method == 'POST':
        sv = models.CaseDetails()
        sv.caseImage = request.FILES['caseImage']
        sv.caseName, caseName = request.POST['caseName'], request.POST['caseName']
        sv.caseRate = request.POST['caseRate']
        sv.save()
        cur.execute('create table ' + caseName.lower().replace(" ", "") +
                    '(id integer primary key auto_increment, phoneName varchar(25) Not Null);')
        cur.execute("select * from PhoneDetails;")
        phones = cur.fetchall()
        for i in phones:
            cur.execute("insert into " + caseName.lower().replace(" ", "") + " (phoneName) values ('" + i[1] + "')")
        return render(request, 'admin/AddCase.html', {'cases' : cases})
    else:
        return render(request, 'admin/AddCase.html', {'cases' : cases})


def addDesign(request):
    cur.execute('select * from CaseDetails;')
    cases = cur.fetchall()
    case = []
    for i in cases:
        case.append(i[2])
    if request.method == 'POST':
        sv = models.DesignDetails()
        sv.DesignImage = request.FILES['designImage']
        sv.DesignName, DesignName = request.POST['designName'], request.POST['designName']
        sv.CaseName, caseName = request.POST['caseType'], request.POST['caseType']
        sv.save()
        if caseName == 'all':
            cur.execute('select * from CaseDetails;')
            cases = cur.fetchall()
            for i in cases:
                cur.execute("alter table " + i[2].lower().replace(" ", "") + " add column " +
                            DesignName.lower().replace(" ", "") + " varchar(10) default 'yes' ")
        else:
            cur.execute("alter table " + caseName.lower().replace(" ", "") + " add column " +
                        DesignName.lower().replace(" ", "") + " varchar(10) default 'yes' ")
        return render(request, 'admin/AddDesign.html', {'case': case})
    else:
        return render(request, 'admin/AddDesign.html', {'case': case})


def addPhone(request):
    if request.method == "POST":
        sv = models.PhoneDetails()
        sv.PhoneName, PhoneName = request.POST['PhoneName'], request.POST['PhoneName']
        sv.save()
        cur.execute('select * from CaseDetails')
        cases = cur.fetchall()
        for i in cases:
            cur.execute("insert into " + i[2].lower().replace(" ", "") + " (phoneName) values ('" + PhoneName + "')")
            
        return render(request, 'admin/AddPhone.html')
    else:
        return render(request, 'admin/AddPhone.html')


def editStock(request):
    cur.execute('''select * from CaseDetails;''')
    pics = cur.fetchall()
    data = []
    for i in pics:
        data.append([i[1], i[2], i[3]])
    return render(request, 'admin/AdminCaseView.html', {'products': reversed(data)})


def editCasePage(request, ctype):
    cur.execute('select * from CaseDetails where casename = "' + ctype + '";')
    data = cur.fetchone()
    if request.method == 'POST':
        caseDetails = models.CaseDetails.objects.get(caseName = ctype)
        try:
            caseDetails.caseImage = request.FILES['caseImage']
        except:
            pass
        finally:
            caseDetails.caseName, caseName = request.POST['caseName'], request.POST['caseName']
            caseDetails.caseRate = request.POST['caseRate']
            caseDetails.save()
        cur.execute(
            f'ALTER TABLE {ctype.lower().replace(" ", "")} RENAME {caseName.lower().replace(" ", "")}')
        return redirect('edit-stock')
    else:
        return render(request, 'admin/AdminEditCase.html', {'values': list(data)})


def deleteCase(request, ctype):
    cur.execute("select caseImage from CaseDetails where caseName = '"+ctype+"';")
    Image = cur.fetchone() 
    os.remove('media/' + Image[0])
    cur.execute("drop table " + ctype.lower().replace(" ", "") + ";")
    cur.execute("delete from CaseDetails where caseName = '" + ctype + "';")
    return redirect('edit-stock')


def adminViewDesign(request, ctype):
    cur.execute("select * from DesignDetails where casename = '" + ctype + "';")
    pics = cur.fetchall()
    data = []
    for i in pics:
        data.append([i[1], i[3], i[2]])
    return render(request, 'admin/AdminDesignView.html', {'products': reversed(data)})


def adminEditDesign(request, ctype, dtype):
    cur.execute('select * from DesignDetails where DesignName = "' + dtype + '";')
    data = cur.fetchone()
    print(data)     
    if request.method == 'POST':
        designDetails = models.DesignDetails.objects.get(DesignName = dtype)
        try:
            designDetails.DesignImage = request.FILES['caseImage']
        except:
            pass
        finally: 
            designDetails.CaseName = ctype
            designDetails.DesignName, designName = request.POST['caseName'], request.POST['caseName']
            designDetails.save()
        cur.execute(
            f' ALTER TABLE {ctype.lower().replace(" ", "")} RENAME COLUMN {dtype.lower().replace(" ", "")} to {designName.lower().replace(" ", "")};')
        return redirect('adminViewCase', ctype = ctype)
    else:
        return render(request, 'admin/AdminEditDesign.html', {'values': list(data)})
    

def deleteDesign(request, ctype, dtype):
    cur.execute("select DesignImage from DesignDetails where DesignName = '"+dtype+"';")
    Image = cur.fetchone() 
    print(Image)
    os.remove('media/' + Image[0])
    cur.execute("alter table " + ctype.lower().replace(" ", "") + " drop column " + dtype + ";")
    cur.execute("delete from DesignDetails where DesignName = '" + dtype + "';")
    return redirect('adminViewCase', ctype = ctype)


def updateStock(request, ctype, dtype):
    cur.execute('select phonename, ' + dtype.lower().replace(" ", "") + ' from ' + ctype.lower().replace(" ", "") + ';')
    phones = cur.fetchall()
    cur.execute(
        'select DesignImage from DesignDetails where casename = "' + ctype + '"')
    design = cur.fetchone()
    phoneList = {}
    for i in phones:
        phoneList[i[0]] = i[1]
    phoneListJson = json.dumps(phoneList)
    if request.method == 'POST':
        PhoneName = request.POST['phoneName']
        stock = request.POST['stockRes']
        if stock != '0':
            cur.execute(f'update {ctype.lower().replace(" ", "")} set {dtype.lower().replace(" ", "")} = "{stock}" where phoneName ="{PhoneName}"')
        return redirect('adminViewCase', ctype = ctype)
    else:
        return render(request, 'admin/AdminEditStock.html', {'design': design[0], 'phoneStock': phoneListJson, 'c_dtype': [ctype, dtype]})
