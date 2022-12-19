import json

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
    if request.method == 'POST':
        sv = models.CaseDetails()
        sv.caseImage = request.FILES['caseImage']
        sv.caseName, caseName = request.POST['caseName'], request.POST['caseName']
        sv.caseRate = request.POST['caseRate']
        sv.save()
        cur.execute('create table ' + caseName.replace(" ", "") +
                    '(id integer primary key auto_increment, phoneName varchar(25) Not Null);')
        return render(request, 'admin/AddCase.html')
    else:
        return render(request, 'admin/AddCase.html')


def addDesign(request):
    cur.execute('select * from caseDetails;')
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
            cur.execute('select * from casedetails;')
            cases = cur.fetchall()
            for i in cases:
                cur.execute("alter table " + i[2].replace(" ", "") + " add column " +
                            DesignName.replace(" ", "") + " varchar(10) default 'yes' ")
        else:
            cur.execute("alter table " + caseName.replace(" ", "") + " add column " +
                        DesignName.replace(" ", "") + " varchar(10) default 'yes' ")
        return render(request, 'admin/AddDesign.html', {'case': case})
    else:
        return render(request, 'admin/AddDesign.html', {'case': case})


def addPhone(request):
    if request.method == "POST":
        sv = models.PhoneDetails()
        sv.PhoneName, PhoneName = request.POST['PhoneName'], request.POST['PhoneName']
        sv.save()
        cur.execute('select * from caseDetails')
        cases = cur.fetchall()
        for i in cases:
            print(i[2])
        cur.execute("insert into " +
                    i[2] + " (phoneName) values ('" + PhoneName + "')")

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


def searchCase(request, type):
    cur.execute('select * from DesignDetails where casename = "' + type + '";')
    pics = cur.fetchall()
    data = []
    for i in pics:
        data.append([i[1], i[3], i[2]])
    return render(request, 'SearchCase.html', {'products': reversed(data), 'type': type})


def searchDesign(request, ctype, dtype):
    cur.execute('select phonename, ' + dtype + ' from ' + ctype.lower() + ';')
    phones = cur.fetchall()
    cur.execute(
        'select DesignImage from DesignDetails where casename = "' + ctype + '"')
    design = cur.fetchone()

    print(phones)
    phoneList = {}
    for i in phones:
        phoneList[i[0]] = i[1]

    phoneListJson = json.dumps(phoneList)
    return render(request, 'SearchStock.html', {'design': design[0], 'phoneStock': phoneListJson})


def editCasePage(request, ctype):
    cur.execute('select * from CaseDetails where casename = "' + ctype + '";')
    data = cur.fetchone()
    if request.method == 'POST':
        caseDetails = models.CaseDetails.objects.get(caseName=ctype)
        caseDetails.caseImage = request.FILES['caseImage']
        caseDetails.caseName, caseName = request.POST['caseName'], request.POST['caseName']
        caseDetails.caseRate = request.POST['caseRate']
        caseDetails.save()
        cur.execute('show tables;')
        print(cur)
        cur.execute(
            f'ALTER TABLE {ctype.replace(" ", "")} RENAME {caseName.replace(" ", "")}')
        return redirect('edit-stock')
    else:
        return render(request, 'admin/AdminEditCase.html', {'values': list(data)})


def adminViewDesign(request, ctype):
    cur.execute("select * from DesignDetails where casename = '" + ctype + "';")
    pics = cur.fetchall()
    data = []
    for i in pics:
        data.append([i[1], i[3], i[2]])
    return render(request, 'admin/AdminDesignView.html', {'products': reversed(data), 'type': type})
