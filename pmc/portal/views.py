from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import TemplateView
from portal.forms import LoginForm, HomeForm, RegisterForm, AddProdForm, CertAccessForm, SelTestLabForm,AddTBresultsForm
from portal.forms import AddSamplesForm, AddTresultsForm, ViewTresultsForm, ViewDetCertForm, ViewTCertForm
import datetime
import MySQLdb

from portal.constants import MYSQL_DB, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER

# PMC Views!! -- Pramod

#RegisterView handles Registration functionality
#Inserts into Manufacturer or Testlab based on usertype field
class RegisterView(TemplateView):
    template_name = 'portal/register.html'

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        Message = ''
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            emailid = form.cleaned_data['emailid']
            phonenumber = form.cleaned_data['phonenumber']
            contactperson = form.cleaned_data['contactperson']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            usertype = form.cleaned_data['usertype']

        #    db = MySQLdb.connect("localhost", "root", "admin123.", "pmc_db")
            print(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
            db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
            cursor = db.cursor()
            print(usertype)
            try:
                if usertype == "1":
                    print("Inserting into Manufacturer")
                    cursor.execute(
                    """INSERT INTO Manufacturer (ManufacturerName, ManufactuerAuthority, PhoneNumber, Address, EmaiID, username, password) VALUES(%s, %s, %s, %s, %s, %s, %s)""",(name, contactperson, phonenumber, address, emailid, username, password))
                    Message = 'Manufacturer registration is Successful. Please Login to access portal'
                    db.commit()
                else:
                    print("Inserting into TestLab")
                    cursor.execute(
                    """INSERT INTO TestLab (TestLabName, TestLabAuthority, PhoneNumber, Address, EmaiID, username, password) VALUES(%s, %s, %s, %s, %s, %s, %s)""",(name, contactperson, phonenumber, address, emailid, username, password))
                    Message = 'TestLab registration is Successful. Please Login to access portal'
                    db.commit()

            except Exception as e:
                print("Error: Inserting data into mysqldb - Registration: ", e)
                Message = "There is an Exception in the form details, Please check and resubmit form: "
                db.rollback()

            db.close()
            form = RegisterForm()

            context = {'message': Message}
            print(context)
            return render(request, 'portal/message.html', context)

        else:
             Message = "PhoneNumber is not valid, Please enter 10-digit valid PhoneNumber"
             context = {'message': Message}
             print(context)
             return render(request, 'portal/message.html', context)


#Login View handles PMC portal login
#First searches username in Manufacturer then Testlab - Sets cookie on Success
#If not found throws Message to user.
class LoginView(TemplateView):
    template_name = 'portal/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        type = ''
        name = ''
        Message = ''
        if form.is_valid():
            usr = form.cleaned_data['username']
            pwd = form.cleaned_data['password']

        #    db = MySQLdb.connect("localhost", "root", "admin123.", "pmc_db")
            print(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
            db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
            cursor = db.cursor()
            print(cursor)
            valicred1 = "SELECT ManufacturerName FROM Manufacturer where username = \"%s\" AND password= \"%s\" " % (usr, pwd)
            valicred2 = "SELECT TestLabName FROM TestLab where username = \"%s\" AND password= \"%s\" " % (usr, pwd)
            try:
                cursor.execute(valicred1)
                mv1 = cursor.fetchone()
                print(mv1)
                if not mv1:
                    print("Not Manufacturer")
                    cursor.execute(valicred2)
                    mv2 = cursor.fetchone()
                    if not mv2:
                        print("Not valid credentials")
                        type = "Invalid"
                        Message = "Invalid credentials, Please login with valid Username/Password!"
                    else:
                        print("TestLab")
                        for row in mv2:
                             name = row
                             type = "TestLab"
                else:
                    print("Manufacturer")
                    for row in mv1:
                        name = row
                        type = "Manufacturer"

            except Exception as e:
                Message= "DB Connection Exception. Please contact administrator."

            db.close()
            form = LoginForm()

        context = {'name': name}
        print(context)
        if type == "Manufacturer":
          #  return render(request, 'portal/manuhome.html', context)
            response = render(request, 'portal/manuhome.html', context)
            response.set_cookie('last_connection', datetime.datetime.now())
            response.set_cookie('ManufacturerName', name )
            return response
        elif type == "TestLab":
         #   return render(request, 'portal/testlabhome.html', context)
            response = render(request, 'portal/testlabhome.html', context)
            response.set_cookie('last_connection', datetime.datetime.now())
            response.set_cookie('TestlabName', name )
            return response
        else:
            context = {'message': Message}
            print(context)
            return render(request, 'portal/message.html', context)



#HomeView handles Search for Product Certification feature
class HomeView(TemplateView):
    template_name = 'portal/index.html'

    def get(self, request):
        form = HomeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        productID = ''
        verdict = ''
        certification =''
        results = ''
        form = HomeForm(request.POST)
        if form.is_valid():
            prodmdl = form.cleaned_data['modelno']
        #    db = MySQLdb.connect("localhost", "root", "admin123.", "pmc_db")
            print(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
            db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
            cursor = db.cursor()
            print(cursor)
            sqlmpower = "SELECT verdict FROM certification where ProductModel = \"%s\" " % prodmdl
            print(sqlmpower)
            try:
                cursor.execute(sqlmpower)
                mv = cursor.fetchone()
                print(mv)
                if not mv:
                    print("Certification details not available")
                    certification = 'Not Certified'
                else:
                    for row in mv:
                        verdict = row
                        if verdict == "PASS":
                            certification= 'Certified'
                            sqlp = "Select allowuseraccess from certificationaccess where ProductModel = \"%s\" " % prodmdl
                            cursor.execute(sqlp)
                            mv = cursor.fetchone()
                            print(mv)
                            if not mv:
                                print("product not tested")
                            else:
                                sqlmpower1 = "SELECT Sequence, Verdict FROM testreport where projectno = (Select projectno from tests where productmodel = \"%s\")" % prodmdl;
                                print(sqlmpower1)
                                cursor.execute(sqlmpower1)
                                results = cursor.fetchall()
                                print(results)
                        else:
                            certification = 'Not Certified'

            except Exception as e:
                print("Error: Fetching data from mysqldb - Home (search product): ", e)
                Message = e

            db.close()
            form = HomeForm()
        context = {'productID': productID, 'verdict' : verdict , 'certification' : certification, 'results' : results}
        print(context)
        return render(request, 'portal/certresults.html', context)


## Manufacturer Views ##
#View to add Product
class AddProdView(TemplateView):
    template_name = 'portal/addprod.html'

    def get(self, request):
        form = AddProdForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AddProdForm(request.POST)
        Message = ''
        if form.is_valid():
            prodmodel1 = form.cleaned_data['prodmodel']
    #        manuname1 = form.cleaned_data['manuname']
            modtech1 = form.cleaned_data['modtech']
            manudate1 = form.cleaned_data['manudate']
            mIsc1 = form.cleaned_data['mIsc']
            mVoc1 = form.cleaned_data['mVoc']
            mImp1 = form.cleaned_data['mImp']
            mVmp1 = form.cleaned_data['mVmp']
            mFF1 = form.cleaned_data['mFF']
            mPmp1 = form.cleaned_data['mPmp']

            manuname1 = request.COOKIES.get('ManufacturerName')
        #    db = MySQLdb.connect("localhost", "root", "admin123.", "pmc_db")
            print(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
            db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
            cursor = db.cursor()
            try:
                    print("Inserting into Products")
                    sql = """INSERT INTO product (ProductModel, ManufacturerName, ModuleTechnology, ManufacturedDate, mIsc, mVoc, mImp, mVmp, mFF, mPmp) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",(prodmodel1, manuname1, modtech1, manudate1, mIsc1, mVoc1, mImp1, mVmp1, mFF1, mPmp1)
                    print(sql)
                    cursor.execute(
                    """INSERT INTO product (ProductModel, ManufacturerName, ModuleTechnology, ManufacturedDate, mIsc, mVoc, mImp, mVmp, mFF, mPmp) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",(prodmodel1, manuname1, modtech1, manudate1, mIsc1, mVoc1, mImp1, mVmp1, mFF1, mPmp1))
                    Message = 'Product added Successfully!'
                    db.commit()

            except Exception as e:
                print("Error: Inserting data into mysqldb: ", e)
                Message = "There is an Exception in the form details, Please check and resubmit form: "
                db.rollback()

            db.close()
            form = AddProdForm()
        context = {'message': Message}
        print(context)
        return render(request, 'portal/manumsg.html', context)


#View to Select Testlab for product testing
class SelTestLabView(TemplateView):
    template_name = 'portal/seltestlab.html'

    def get(self, request):
        form = SelTestLabForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SelTestLabForm(request.POST)
        Message = ''
        if form.is_valid():
            prodmodel = form.cleaned_data['prodmodel']
            testlab = form.cleaned_data['testlab']

        #    db = MySQLdb.connect("localhost", "root", "admin123.", "pmc_db")
            print(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
            db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
            cursor = db.cursor()
            print(testlab)
            try:
                print("Inserting into Tests table")
                cursor.execute("""INSERT INTO Tests (ProductModel, TestLabName) VALUES(%s, %s)""",(prodmodel, testlab))
                Message = 'Selecting TestLab for Product is Successful!'
                db.commit()
            except Exception as e:
                print("Error: Inserting data into mysqldb: ", e)
                Message = "There is an Exception in the form details, Please check and resubmit form: "
                db.rollback()

            db.close()
            form = SelTestLabForm()

        context = {'message': Message}
        print(context)
        return render(request, 'portal/manumsg.html', context)


# View to allow access to user to view detailed certification
class AllowAccessView(TemplateView):
        template_name = 'portal/allowaccess.html'

        def get(self, request):
            form = CertAccessForm()
            return render(request, self.template_name, {'form': form})

        def post(self, request):
            form = CertAccessForm(request.POST)
            Message = ''
            if form.is_valid():
         #       manuname = form.cleaned_data['manuname']
                prodmodel = form.cleaned_data['prodmodel']
                allowuser = form.cleaned_data['allowuser']

                manuname = request.COOKIES.get('ManufacturerName')
            #    db = MySQLdb.connect("localhost", "root", "admin123.", "pmc_db")

                print(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
                db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)

                cursor = db.cursor()
                print(allowuser)
                try:
                        print("Inserting into CertificationAccess table")
                        cursor.execute(
                            """INSERT INTO CertificationAccess (ManufacturerName, ProductModel, AllowUserAccess) VALUES(%s, %s, %s)""",(manuname, prodmodel, allowuser ))
                        Message = 'User Certification Access Updated Successful!'
                        db.commit()
                except Exception as e:
                    print("Error: Inserting data into mysqldb: ", e)
                    Message = "There is an Exception in the form details, Please check and resubmit form: "
                    db.rollback()

                db.close()
                form = CertAccessForm()

            context = {'message': Message}
            print(context)
            return render(request, 'portal/manumsg.html', context)

#View Products
def viewprods(request):
   # db = MySQLdb.connect("localhost", "root", "admin123.", "pmc_db")
    print(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
    cursor = db.cursor()
    print(cursor)
    sqlmpower = "SELECT ProductModel, ModuleTechnology, ManufacturedDate,mIsc ,mVoc, mImp, mVmp, mFF, mPmp FROM product where ManufacturerName = \"%s\" " % request.COOKIES.get('ManufacturerName');
    print(sqlmpower)
    try:
        cursor.execute(sqlmpower)
        results = cursor.fetchall()
        print(results)

    except Exception as e:
        print("Error: Fetching data from mysqldb: ", e)
        Message = e
    db.close()

    context = {'results': results}
    print(context)
    return render(request, 'portal/viewprods.html', context)

#View to handle detailed certification
class viewdetcert(TemplateView):
    template_name = 'portal/detcertform.html'

    def get(self, request):
        form = ViewDetCertForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ViewDetCertForm(request.POST)

        if form.is_valid():
            prodmdl = form.cleaned_data['prodmdl']

       #     db = MySQLdb.connect("localhost", "root", "admin123.", "pmc_db")
            print(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
            db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
            cursor = db.cursor()
            print(cursor)

            sqlmpower = "SELECT Sequence, Verdict FROM testreport where projectno = (Select projectno from tests where productmodel = \"%s\")" % prodmdl;
            print(sqlmpower)

            try:
                cursor.execute(sqlmpower)
                results = cursor.fetchall()
                print(results)

            except Exception as e:
                print("Error: Fetching data from mysqldb: ", e)
                Message = e
            db.close()

        print("Sending results to Template")
        context = {'results': results, 'prodmdl': prodmdl}
        print(context)
        return render(request, 'portal/viewdetcerti.html', context)


## TestLab Views ##
#For adding initial baseline tests
class AddTBresultsView(TemplateView):
    template_name = 'portal/baseline.html'

    def get(self, request):
        form = AddTBresultsForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AddTBresultsForm(request.POST)
        Message = ''
        prevResult=''
        prevSeqResult=''
        if form.is_valid():
            projno = form.cleaned_data['projno']
            sampleid = form.cleaned_data['sampleid']
            seq = 'Z' # Z treated as Baseline test due to Char constraint in DB
          #  testname = form.cleaned_data['testname']
            testname = 'Baseline'
            testdate = form.cleaned_data['testdate']
            tIsc = form.cleaned_data['tIsc']
            tVoc = form.cleaned_data['tVoc']
            tImp = form.cleaned_data['tImp']
            tVmp = form.cleaned_data['tVmp']
            tFF = form.cleaned_data['tFF']
            tPmp = form.cleaned_data['tPmp']

        #    db = MySQLdb.connect("localhost", "root", "admin123.", "pmc_db")
            print(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
            db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
            cursor = db.cursor()

            sqlmpower = "SELECT mPmp FROM Product where ProductModel = (select productmodel from tests where projectno = %s)" % int(projno)
            print(sqlmpower)
            try:
                cursor.execute(sqlmpower)
                mv = cursor.fetchone()
                print(mv)
                for row in mv:
                    ratedPower = row
                    print(ratedPower)
                RatedOutputPower = ratedPower
            except Exception as e:
                print("Error Getting data from mysqldb")
                Message="There is an Exception in the form details, Please check: " + str(e)

            BaselineOutputPower = tPmp
            print("-------- MFG Rated Output Power--------", RatedOutputPower)
            print("-------- Baseline Output Power---------", BaselineOutputPower)

            print("Checking: Initial (Baseline) power output must be within +/-10% of rated power")
            bpert = (RatedOutputPower - BaselineOutputPower) / RatedOutputPower
            bpert = bpert * 100
            bverd = 'PASS'
            if abs(bpert) < 10.0:
                print("PASS", bpert)
            else:
                print("FAIL", bpert)
                bverd = 'FAIL'

            try:
                    print("Inserting into testresults")
                    sql = """INSERT INTO testresults (ProjectNo, SampleID, Sequence, TestName, TestDate, tIsc, tVoc, tImp, tVmp, tFF, tPmp) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",(int(projno), int(sampleid), seq, testname, testdate, tIsc, tVoc, tImp, tVmp, tFF, tPmp)
                    print(sql)
                    cursor.execute(
                    """INSERT INTO testresults (ProjectNo, SampleID, Sequence, TestName, TestDate, tIsc, tVoc, tImp, tVmp, tFF, tPmp) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",(int(projno), int(sampleid), seq, testname, testdate, tIsc, tVoc, tImp, tVmp, tFF, tPmp))
                    Message = 'Baseline Test results added Successfully!'
                    db.commit()

            except Exception as e:
                print("Error: Inserting data into mysqldb: ", e)
                Message = "There is an Exception in the form details, Please check testresults: "
                db.rollback()

            prevResult = "SELECT Verdict FROM testreport where projectno = %s AND sequence= \"%s\" " % (int(projno), str(seq))

            try:
                cursor.execute(prevResult)
                mv = cursor.fetchone()
                if not mv:
                    print("Previous results not available")
                    prevSeqResult = 'null'
                else:
                    for row in mv:
                        presult = row
                        prevSeqResult = presult
            except Exception as e:
                print("Error Getting data from mysqldb -- previous baseline result")
                Message = "There is an Exception in the form details, Please check testreport: "

            try:
                if prevSeqResult == 'null':
                    print("First Entry to Report Table")
                    cursor.execute("""INSERT INTO testreport (ProjectNo, Sequence, Verdict) VALUES(%s, %s, %s)""",(int(projno), seq, bverd))
                    db.commit()
                elif prevSeqResult == 'PASS' and bverd == 'PASS':
                    print("Previous Result: ", prevSeqResult, "Current Test Result: ", bverd)
                elif prevSeqResult == 'FAIL' and bverd == 'PASS':
                    print("Previous Result: ", prevSeqResult, "Current Test Result: ", bverd)
                    print("Previous sample failed -- Sequence Failed")
                elif prevSeqResult == 'PASS' and bverd == 'FAIL':
                    print("Previous Result: ", prevSeqResult, "Current Test Result: ", bverd)
                    cursor.execute("""UPDATE testreport SET verdict= %s WHERE ProjectNo= %s AND Sequence = %s""", (bverd, int(projno), seq))
                    db.commit()
                    print("Previous sample failed -- Sequence Failed")
                elif prevSeqResult == 'FAIL' and bverd == 'FAIL':
                    print("Previous Result: ", prevSeqResult, "Current Test Result: ", bverd)
                    print("Samples failed -- Baseline(Initial) Tests Failed -- Product Failed ")
            except Exception as e:
                print("Error Inserting report data into mysqldb -- baseline test")
                Message = "There is an Exception in the form details, Please check testreport Baseline: "
                db.rollback()

            db.close()
            form = AddTBresultsForm()

        context = {'message': Message}
        print(context)
        return render(request, 'portal/testlabmsg.html', context)


#view to add samples
class AddSamplesView(TemplateView):
        template_name = 'portal/addsamples.html'

        def get(self, request):
            form = AddSamplesForm()
            return render(request, self.template_name, {'form': form})

        def post(self, request):
            form = AddSamplesForm(request.POST)
            Message = ''
            count=1
            scount=0
            if form.is_valid():
                projno = form.cleaned_data['projno']
                samplescount = form.cleaned_data['samplescount']

            #    db = MySQLdb.connect("localhost", "root", "admin123.", "pmc_db")
                print(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
                db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
                cursor = db.cursor()
                scount = int(samplescount)
                try:
                    print("Inserting into Samples table")
                    while count<=scount:
                        cursor.execute("""INSERT INTO Samples (ProjectNo, SampleID) VALUES(%s, %s)""",(int(projno), int(count)))
                        db.commit()
                        count = count+1
                    Message = 'Samples are added to the Project Successfully!'

                except Exception as e:
                    print("Error: Inserting data into mysqldb: ", e)
                    Message = "Samples are already added to the Project. "
                    db.rollback()

                db.close()
                form = AddSamplesForm()

            context = {'message': Message}
            print(context)
            return render(request, 'portal/testlabmsg.html', context)


#View to add Stress test results
class AddTresultsView(TemplateView):
    template_name = 'portal/tresults.html'

    def get(self, request):
        form = AddTresultsForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AddTresultsForm(request.POST)
        Message = ''
        prevResult=''
        prevSeqResult=''
        base = 'temp'
        BaselineOutputPower=1
        PowerAfterStressTest=0
        flag = 'yes'
        if form.is_valid():
            projno = form.cleaned_data['projno']
            sampleid = form.cleaned_data['sampleid']
            seq = form.cleaned_data['seq']
            testname = form.cleaned_data['testname']
            testdate = form.cleaned_data['testdate']
            tIsc = form.cleaned_data['tIsc']
            tVoc = form.cleaned_data['tVoc']
            tImp = form.cleaned_data['tImp']
            tVmp = form.cleaned_data['tVmp']
            tFF = form.cleaned_data['tFF']
            tPmp = form.cleaned_data['tPmp']

        #    db = MySQLdb.connect("localhost", "root", "admin123.", "pmc_db")
            print(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
            db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
            cursor = db.cursor()

            try:
                print("Inserting into testresults")
                sql = """INSERT INTO testresults (ProjectNo, SampleID, Sequence, TestName, TestDate, tIsc, tVoc, tImp, tVmp, tFF, tPmp) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",(int(projno), int(sampleid), seq, testname, testdate, tIsc, tVoc, tImp, tVmp, tFF, tPmp)
                print(sql)
                cursor.execute(
                """INSERT INTO testresults (ProjectNo, SampleID, Sequence, TestName, TestDate, tIsc, tVoc, tImp, tVmp, tFF, tPmp) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",(int(projno), int(sampleid), seq, testname, testdate, tIsc, tVoc, tImp, tVmp, tFF, tPmp))
                Message = 'Stress Test results added Successfully!'
                db.commit()

            except Exception as e:
                print("Error: Inserting data into mysqldb: ", e)
                Message = "There is an Exception in the form details, Please check testresults: "
                db.rollback()


            sqlmpower = "SELECT tPmp FROM testresults where sampleID= %s AND sequence = 'Z' AND  projectno = %s" % (int(sampleid), int(projno))
            print(sqlmpower)

            try:
                cursor.execute(sqlmpower)
                results = cursor.fetchone()
                if not results:
                    print("Baseline values are not available")
                    base = 'null'
                    flag = 'no'
                else:
                    for row in results:
                        ratedPower = row
                        print("---------Baseline Values--------"
                              , "Output Power=%f" % \
                              (ratedPower))
                        BaselineOutputPower = ratedPower
            except Exception as e:
                print("Error Getting data from mysqldb")
                Message="There is an Exception in the form details, Please check: "

        if flag == 'no':
            Message = "No Baseline Values for Sample. Please add Baseline test results first."
        else:
            PowerAfterStressTest = float(tPmp)
            print("Checking: No performance parameter must decrease by more than 5% after a stress test")
            if base == 'null':
                print("No performance parameters are checked as baseline values are not available")
            else:
                pert1 = (BaselineOutputPower - PowerAfterStressTest) / BaselineOutputPower
                pert1 = pert1 * 100
                overd = 'PASS'
                if abs(pert1) <= 5.0:
                    print("PASS", pert1)
                else:
                    print("FAIL", pert1)
                    overd = 'FAIL'

            prevResult = "SELECT Verdict FROM testreport where projectno = %s AND sequence= \"%s\" " % (int(projno), str(seq))
            print(prevResult)
            try:
                cursor.execute(prevResult)
                mv = cursor.fetchone()
                if not mv:
                    print("Previous results not available")
                    prevSeqResult = 'null'
                else:
                    for row in mv:
                        presult = row
                        prevSeqResult = presult
            except Exception as e:
                print("Error Getting data from mysqldb -- previous stress test result")
                Message = "There is an Exception in the form details, Please check testreport: "

            try:
                if prevSeqResult == 'null':
                    print("First Entry to Report Table")
                    cursor.execute("""INSERT INTO testreport (ProjectNo, Sequence, Verdict) VALUES(%s, %s, %s)""",(int(projno), seq, overd))
                    db.commit()
                elif prevSeqResult == 'PASS' and overd == 'PASS':
                    print("Previous Result: ", prevSeqResult, "Current Test Result: ", overd)
                elif prevSeqResult == 'FAIL' and overd == 'PASS':
                    print("Previous Result: ", prevSeqResult, "Current Test Result: ", overd)
                    print("Previous sample failed -- Sequence Failed")
                elif prevSeqResult == 'PASS' and overd == 'FAIL':
                    print("Previous Result: ", prevSeqResult, "Current Test Result: ", overd)
                    cursor.execute("""UPDATE testreport SET verdict= %s WHERE ProjectNo= %s AND Sequence = %s""", (overd, int(projno), seq))
                    db.commit()
                    print("Previous sample failed -- Sequence Failed")
                elif prevSeqResult == 'FAIL' and overd == 'FAIL':
                    print("Previous Result: ", prevSeqResult, "Current Test Result: ", overd)
            except Exception as e:
                print("Error Inserting report data into mysqldb -- stress test")
                Message = "There is an Exception in the form details, Please check testreport stresstests : "
                db.rollback()

            db.close()
            form = AddTresultsForm()

        context = {'message': Message}
        print(context)
        return render(request, 'portal/testlabmsg.html', context)



#View to view Test Results
class ViewTresultsView(TemplateView):
    template_name = 'portal/viewresform.html'

    def get(self, request):
        form = ViewTresultsForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ViewTresultsForm(request.POST)

        if form.is_valid():
            projno = form.cleaned_data['projno']

        #    db = MySQLdb.connect("localhost", "root", "admin123.", "pmc_db")
            print(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
            db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
            cursor = db.cursor()
            print(cursor)

            sqlmpower = "SELECT ProjectNo, SampleID, Sequence, TestName, tIsc, tVoc, tImp, tVmp, tFF, tPmp FROM testresults where projectno = %s" % int(projno);
            print(sqlmpower)

            try:
                cursor.execute(sqlmpower)
                results = cursor.fetchall()
                print(results)

            except Exception as e:
                print("Error: Fetching data from mysqldb: ", e)
                Message = e
            db.close()

        print("Sending results to Template")
        context = {'results': results, 'projno' : projno}
        print(context)
        return render(request, 'portal/viewtresults.html', context)


# View to handle detailed certification
class viewTcert(TemplateView):
        template_name = 'portal/viewtestcertiform.html'

        def get(self, request):
            form = ViewTCertForm()
            return render(request, self.template_name, {'form': form})

        def post(self, request):
            form = ViewTCertForm(request.POST)

            if form.is_valid():
                projno = form.cleaned_data['projno']

            #    db = MySQLdb.connect("localhost", "root", "admin123.", "pmc_db")
                print(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
                db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
                cursor = db.cursor()
                print(cursor)

                sqlmpower = "SELECT Sequence, Verdict FROM testreport where projectno = %s" % int(projno);
                print(sqlmpower)

                try:
                    cursor.execute(sqlmpower)
                    results = cursor.fetchall()
                    print(results)

                except Exception as e:
                    print("Error: Fetching data from mysqldb: ", e)
                    Message = e
                db.close()

            print("Sending results to Template")
            context = {'results': results, 'projno': projno}
            print(context)
            return render(request, 'portal/viewtcerti.html', context)


#Logout view
def logout(request):
    Message = 'Successfully logged out of PMC portal!'
    context = {'message': Message}
    print(context)
    response = render(request, 'portal/message.html', context)
    response.delete_cookie('ManufacturerName')
    response.delete_cookie('TestlabName')
    return response

#failanalysis view
def failanalysis(request):

 #   db = MySQLdb.connect("localhost", "root", "admin123.", "pmc_db")
    print(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
    cursor = db.cursor()
    print(cursor)
    list = ["A", "B", "C"]
    x1 =0
    x2 =0
    x3 =0
    x4 =0
    x5 =0

    for f in list:
      total = 1
      failed = 0
      sqlTotal = "SELECT count(ProjectNo) FROM testreport where Sequence = \"%s\" " % f;
      sqlFail =  "SELECT count(ProjectNo) FROM testreport where verdict=\"FAIL\" and Sequence = \"%s\" " % f;
      print(sqlTotal)
      try:
          cursor.execute(sqlTotal)
          mv1 = cursor.fetchone()
          print(mv1)
          if not mv1:
              print("No Sequence Results - Failure Analysis")
          else:
               print("Sequence: ", f)
               for row in mv1:
                   if row == 0:
                       total = 1
                   else:
                       total = row

               cursor.execute(sqlFail)
               print(sqlFail)
               mv2 = cursor.fetchone()
               print(mv2)
               if not mv2:
                   print("No Sequence Failed - Failure Analysis ")
               else:
                   print("Sequence: ", f)
                   for row in mv2:
                       failed = row

          if f == "A":
              x2 = (failed/ total) * 100
              x3 = (failed/ total) * 100
              x5 = (failed/ total) * 100
          elif f == "B":
              x1 = (failed/ total) * 100
          elif f == "C":
              x4 = (failed/ total) * 100
      except Exception as e:
        print("Error: Fetching data from mysqldb: ", e)
        Message = '0, 0, 0, 0, 0'
    db.close()
    Message = ''+str(x1)+','+str(x2)+','+str(x3)+','+str(x4)+','+str(x5)
#    Message = '10, 80, 30, 40, 5'
    context = {'message': Message}
    print(context)
    response = render(request, 'portal/failureanalysis.html', context)
    return response

#View Projects - Testlab
def viewprojs(request):
#    db = MySQLdb.connect("localhost", "root", "admin123.", "pmc_db")
    print(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)

    cursor = db.cursor()
    print(cursor)
    sqlmpower = "SELECT ProjectNo, ProductModel FROM tests where testlabName = \"%s\" " % request.COOKIES.get('TestlabName');
    print(sqlmpower)
    try:
        cursor.execute(sqlmpower)
        results = cursor.fetchall()
        print(results)

    except Exception as e:
        print("Error: Fetching data from mysqldb: ", e)
        Message = e
    db.close()

    context = {'results': results}
    print(context)
    return render(request, 'portal/viewprojs.html', context)
