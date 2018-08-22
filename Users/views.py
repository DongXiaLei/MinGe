from django.shortcuts import render,redirect
from django.views.generic.base import View
from django.contrib.auth import authenticate,login
from .forms import LoginForm,ModifypwdForm,AdduserForm
from .models import baseInfo,User,ContactList,education,Work,Resume,AwardInfo,Punish,PositionSincePast,MinGeRelation,FamilyMember,activity
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from collections import Counter
from django.contrib.auth.backends import ModelBackend

#支部人数统计
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(phone=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

def union_dict(*objs):
    _keys = set(sum([obj.keys() for obj in objs],[]))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([obj.get(_key,0) for obj in objs])

def getAgeCount():
    ageSegMent={
        "age0_20":0,
        "age20_25": 0,
        "age25_30": 0,
        "age30_35": 0,
        "age35_40": 0,
        "age40_45": 0,
        "age45_50": 0,
        "age50_55": 0,
        "age55_60": 0,
        "age60_": 0,
    }
    BornDateList=ContactList.objects.all().values('BornDate')
    CurrentYear=datetime.now().year
    for oneBornDate in BornDateList:
        if oneBornDate['BornDate'] is None:
            continue

        BornYear=oneBornDate["BornDate"].year
        diff=CurrentYear-BornYear
        if diff in range(0,20):
            ageSegMent["age0_20"] = ageSegMent["age0_20"]+1
        elif diff in range(20,25):
            ageSegMent["age20_25"] = ageSegMent["age20_25"]+1
        elif diff in range(25,30):
            ageSegMent["age25_30"] = ageSegMent["age25_30"]+1
        elif diff in range(30,35):
            ageSegMent["age30_35"] = ageSegMent["age30_35"] + 1
        elif diff in range(35,40):
            ageSegMent["age35_40"] = ageSegMent["age35_40"] + 1
        elif diff in range(40,45):
            ageSegMent["age40_45"] = ageSegMent["age40_45"] + 1
        elif diff in range(45,50):
            ageSegMent["age45_50"] = ageSegMent["age45_50"] + 1
        elif diff in range(50,55):
            ageSegMent["age50_55"] = ageSegMent["age50_55"] + 1
        elif diff in range(55, 60):
            ageSegMent["age55_60"] = ageSegMent["age55_60"] + 1
        else:
            ageSegMent["age60_"] = ageSegMent["age60_"] + 1
    return ageSegMent

#支部性别统计
# def getGenderCount(zhibuName):
#     manNum=ContactList.objects.filter(gender=u"男", BranchPartyName=zhibuName).count()
#     womanNum = ContactList.objects.filter(gender=u"女",BranchPartyName=zhibuName).count()
#     return {"male":manNum,"female":womanNum}
def getGenderCount():
    manNum=ContactList.objects.filter(gender=u"男",).count()
    womanNum = ContactList.objects.filter(gender=u"女").count()
    return {"male":manNum,"female":womanNum}
#支部学历统计
def getEduExpCount():
    UnderSeniorEduExpName=['高中']
    #专科
    TechniqueEduExpName=['大专','中专','专科']
    UndergraduateEduExpName = ['大学','本科']
    PostgraduateEduExpName=['研究生','硕士']
    DoctorgraduateEduExpName=['博士']

    UnderSeniorCount=ContactList.objects.filter(EduExperience__in=UnderSeniorEduExpName).count()
    UndergraduateCount = ContactList.objects.filter(EduExperience__in=UndergraduateEduExpName).count()
    TechniqueCount = ContactList.objects.filter(EduExperience__in=TechniqueEduExpName).count()
    PostgraduateCount = ContactList.objects.filter(EduExperience__in=PostgraduateEduExpName).count()
    DoctorgraduateCount = ContactList.objects.filter(EduExperience__in=DoctorgraduateEduExpName).count()
    #TODO::注意，这里返回的是dict，使用需注意
    return {
        "undersenior":UnderSeniorCount,
        "technique": TechniqueCount,
        "undergraduate":UndergraduateCount,
        "postgraduate":PostgraduateCount,
        "doctor":DoctorgraduateCount
    }
class ConfigInfo:
    setlist=['民革武昌区工委会一支部', '民革武昌区工委会二支部', '民革武昌区工委会三支部', '民革武昌区工委会四支部', '民革武昌区工委会五支部', '民革武昌区工委会六支部',
     '民革武昌区工委会七支部', '民革武昌区工委会八支部', '民革武昌区工委会九支部']
    urllist = {"url1":'xxx',}
    @classmethod
    def getCorrectDate(cls, dateToformat):
        daterightflag = False
        dateRet=None
        if (not daterightflag):
            try:
                dateRet = datetime.strptime(dateToformat, '%Y年%m月%d日')
                daterightflag = True
            except ValueError:
                pass
        if (not daterightflag):
            try:
                dateRet = datetime.strptime(dateToformat, '%Y-%m-%d')
                daterightflag = True
            except ValueError:
                pass
        if (not daterightflag):
            try:
                dateRet = datetime.strptime(dateToformat, '%Y%m%d')
                daterightflag = True
            except ValueError:
                pass
        if (not daterightflag):
            dateRet = datetime(1990,9,7)
        return  dateRet


def index(request):
    if request.user.is_authenticated():
        return render(request, "index.html", {"user":request.user,"time":datetime.now()})
    else :
        return render(request,"login.html")
def leader(request):
    if request.user.is_authenticated():
        return render(request, "leader.html", {"user":request.user,"time":datetime.now()})
    else :
        return render(request,"login.html")
def activityView(request):
    if request.user.is_authenticated():

        return render(request, "activity.html", {"user":request.user,"time":datetime.now()})
    else :
        return render(request,"login.html")
def logout(request):
    logout(request.user)
    return render(request,"login.html")


class addresslist(View):
    def get(self, request):
        setList =ConfigInfo.setlist
        member = []
        for onename in setList:
            allContact = ContactList.objects.filter(BranchPartyName=onename)
            if allContact:
                member.append(allContact)

        # allContact.query._by=["BranchPartyName"]
        if request.user.is_authenticated():
            return render(request, "addresslist.html",
                          {"allConGroup": member, "user": request.user, "time": datetime.now(),"flag":False})
        else:
            return render(request, "login.html")


class LoginView(View):
    def get(self,request):
        return render(request, "login.html", {})
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            time = datetime.now()
            if user is not None:
                login(request, user)
                if user.is_manager == True:
                    return render(request, "index.html", {"user": user, "time": time})
                else:
                    return render(request, "index.html", {"user": user, "time": time})
            else:
                return render(request, "login.html", {"login_form": login_form, "msg": "用户名或密码错误"})

        else:
            return render(request, "login.html", {"login_form":login_form, "msg": "输入有误，请重新输入"})
class ModifypwdView(View):
    def get(self,request):
        return render(request, "modify_pwd.html", {})
    def post(self,request):
        modifypwd_form = ModifypwdForm(request.POST)
        if modifypwd_form.is_valid():
            user_name = request.POST.get("phone", "")
            pwd = request.POST.get("password","")
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")

            USER=None
            user = None
            try:
                USER = User.objects.get(phone=user_name)
            except :
                return render(request, "modify_pwd.html", {"modify_form":modifypwd_form, "msg": "没有该用户"})
            try:
                user = authenticate(username=user_name, password=pwd)
            except:
                return render(request, "modify_pwd.html", {"modify_form": modifypwd_form, "msg": "密码验证错误"})

            if user is not None:
                if USER:
                    if pwd1 != pwd2:
                        return render(request, "modify_pwd.html", {"modify_form": modifypwd_form, "msg": "两次密码不一致"})
                    else:

                        USER.password = make_password(pwd1)
                        USER.save()
                        return render(request, "login.html")
            else:
                return render(request, "modify_pwd.html", {"modify_form":modifypwd_form, "msg": "用户密码错误"})
        else:
            return render(request,"modify_pwd.html",{"msg": "输入有误，请重新输入"})


class ModifyUser(View):
    def get(self,request):
        userId=request.GET.get('id','0')
        userid=int(userId)
        userInfo=None
        try:
            userInfo=User.objects.get(id=userid)
        except:
            return render(request, "user_manage.html")
        return render(request, "modifyUser.html", {
            "userInfo":userInfo
        })
    def post(self,request):
        adduser_form = AdduserForm(request.POST)
        if adduser_form.is_valid():
            user_name = request.POST.get("username", "")
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")
            phone = request.POST.get("phone","")
            select1 = request.POST.get("select1","")
            select2 = request.POST.get("select2","")
            if phone :
                if pwd1 != pwd2:
                    return render(request, "add_user.html", {"adduser_form":adduser_form, "msg": "两次密码不一致"})
                else:
                    user = User.objects.get(phone=phone)
                    user.username = user_name
                    user.password=make_password(pwd1)
                    user.login_time=datetime.now()
                    if select1 == "1":
                        user.gender = "1"
                    else : user.gender = "0"
                    if select2 == "1":
                        user.is_manager =1
                    else : user.is_manager =0
                    user.save()
                    return render(request, "user_manage.html")
            else:
                return render(request, "add_user.html", {"adduser_form":adduser_form, "msg": "用户不存在"})
        else:
            return render(request,"add_user.html",{"msg": "输入有误，请重新输入"})
def user_manage(request):
    if request.user.is_authenticated():
        user_list = User.objects.all()
        paginator = Paginator(user_list, 1000)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request, "user_manage.html", {"user": request.user,"time":datetime.now(), "guests": contacts})
class delete_user(View):
    def get(self,request):
        userId=request.GET.get('id','0')
        userid=int(userId)
        userInfo=None
        try:
            userInfo=User.objects.get(id=userid)
        except:
            return render(request, "user_manage.html",{"user": request.user,"time":datetime.now()})
        userInfo.delete()
        return render(request, "user_manage.html",{"user": request.user,"time":datetime.now()})
class AdduserView(View):
    def get(self,request):
        if request.user.is_authenticated():
            return render(request, "add_user.html", {"user": request.user, "time": datetime.now()})
        else:
            return render(request, "login.html")
    def post(self,request):
        adduser_form = AdduserForm(request.POST)
        if adduser_form.is_valid():
            user_name = request.POST.get("username", "")
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")
            phone = request.POST.get("phone","")
            select1 = request.POST.get("select1","")
            select2 = request.POST.get("select2","")
            try:
                 phone_veritfy = User.objects.get(phone=phone)
                 return render(request, "add_user.html", {"adduser_form": adduser_form, "msg": "该手机号已存在"})
            except :
                if phone:
                    if pwd1 != pwd2:
                        return render(request, "add_user.html", {"adduser_form": adduser_form, "msg": "两次密码不一致"})
                    else:
                        user = User()
                        user.phone = phone
                        user.username = user_name
                        user.password = make_password(pwd1)
                        user.login_time = datetime.now()
                        if select1 == "1":
                            user.gender = 1
                        else:
                            user.gender = 0
                        if select2 == "1":
                            user.is_manager = 1
                        else:
                            user.is_manager = 0
                        user.save()
                        return render(request, "login.html")
                else:
                    return render(request, "add_user.html", {"adduser_form": adduser_form, "msg": "手机号不能为空"})
        else:
            return render(request,"add_user.html",{"msg": "输入有误，请重新输入"})

def search_name(request):
    search_name = request.POST.get("name", "")
    guest_list = User.objects.filter(Q(username__contains=search_name)|Q(phone__contains=search_name))
    return render(request, "user_manage.html", {"user": request.user, "time": datetime.now(),"guests": guest_list})
def search_userlist(request):
    search_name = request.POST.get("name", "")
    if not search_name=="":
        member = ContactList.objects.filter(Q(name__contains=search_name) | Q(MobilePhone__contains=search_name))
        temp = []
        temp.append(member)
        member = temp
        return render(request, "userlist.html",
                      {"flag": True, "allConGroup": member, "user": request.user, "time": datetime.now(),"msg":""})
    else:
        setList = ConfigInfo.setlist
        member = []
        for onename in setList:
            allContact = ContactList.objects.filter(BranchPartyName=onename)
            if allContact:
                member.append(allContact)
        if request.user.is_authenticated():
            return render(request, "userlist.html",
                          {"flag": True, "allConGroup": member, "user": request.user, "time": datetime.now(),
                           "msg": "输入不能为空，请重新输入！"})
        else:
            return render(request, "login.html")


def search_address(request):

    search_name = request.POST.get("name", "")
    if not search_name=="":
        member = ContactList.objects.filter(Q(name__contains=search_name) | Q(MobilePhone__contains=search_name))
        temp = []
        temp.append(member)
        member = temp
        return render(request, "addresslist.html",
                      {"flag":True,"allConGroup": member, "user": request.user, "time": datetime.now(),"msg":""})
    else:
        setList = ConfigInfo.setlist
        member = []
        for onename in setList:
            allContact = ContactList.objects.filter(BranchPartyName=onename)
            if allContact:
                member.append(allContact)

        # allContact.query._by=["BranchPartyName"]
        if request.user.is_authenticated():
            return render(request, "addresslist.html",
                          {"flag":True,"allConGroup": member, "user": request.user, "time": datetime.now(),"msg":"输入不能为空，请重新输入！"})
        else:
            return render(request, "login.html")




class userlist(View):
    def get(self, request):

        # 测试获取数据的三个函数用
        allgender = getGenderCount()
        allede = getEduExpCount()
        allage = getAgeCount()

        allgenderlist = []
        for key,value in allgender.items():
            allgenderlist.append(value)
        alledelist1 =[]
        alledelist2 = []
        for key,value in allede.items():
            alledelist1.append(key)
            alledelist2.append(value)
        allagelist1 =[]
        allagelist2 = []
        for key,value in allage.items():
            allagelist1.append(key)
            allagelist2.append(value)
        # END 测试获取数据的三个函数用

        setList=ConfigInfo.setlist
        member=[]
        for onename in setList:
            allContact=ContactList.objects.filter(BranchPartyName=onename)
            if allContact:
                member.append(allContact)
        if request.user.is_authenticated():
            if request.user.is_manager:
                return render(request, "userlist.html",
                              {"flag":False, "allConGroup": member, "user": request.user, "time": datetime.now(),
                               "allgender": allgenderlist, "alledelist2": alledelist2, "allagelist2": allagelist2})
            else: return render(request, "login.html",{"msg":"您不是管理员，没有权限查看，请联系联络员解决！"})
        else:
            return render(request, "login.html")

def userinformation(request):
    if request.user.is_authenticated():
        userID = request.GET.get('name', '0')
        if userID == '' or userID == '0':
            return redirect('/index')
        userDis = None
        try:
            userDis = baseInfo.objects.get(name=userID)
        except:
            return render(request, "index.html", {
                "Msg": "读取用户失败，没有这个用户",
            })
        return render(request, "userinformation.html", {
            "Msg": "请修改页面后保存",
            "userinfo": userDis
        })
        username=request.GET.get("name", '0')
        user_info=None
        try:
            user_info = baseInfo.objects.filter(name=username)
        except:
            pass
        return render(request, "userinformation.html",
                      {"user": request.user, "time": datetime.now(), "userinfo": user_info})



    else: return render(request,"login.html")
class userinformation_add(View):
    def get(self,request):
        if request.user.is_authenticated():
             return render(request,"userinformation_add.html",{"user": request.user, "time": datetime.now()})

    def post(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        if not request.user.is_manager:
            return render(request, "login.html")
        #baseinfo表
        name = request.POST.get("name"," ")
        nation = request.POST.get("selectnation"," ")
        Bornplace = request.POST.get("Bornplace"," ")
        partynum = request.POST.get("partynum"," ")
        phonenum = request.POST.get("phonenum"," ")

        nameused = request.POST.get("nameused","")
        nativeplace = request.POST.get("nativeplace","")
        borndate= request.POST.get("borndate","")
        branchname = request.POST.get("branchname","")
        email = request.POST.get("email", "")

        religious = request.POST.get("religious", "")
        IDnum = request.POST.get("IDnum", "")
        branchnnum = request.POST.get("branchnnum", "")

        if ( not(name=='' and IDnum=='' and phonenum=='')):
            BaseInfo = baseInfo()

            BaseInfo.name = name
            BaseInfo.nameUsed = nameused
            BaseInfo.nation=nation
            BaseInfo.NativePlace = nativeplace

            BaseInfo.religious = religious
            BaseInfo.BornPlace=Bornplace
            BaseInfo.BornDate = borndate
            BaseInfo.IDCardNum = IDnum
            BaseInfo.PartyDocuNum = partynum

            BaseInfo.BranchParty = branchname
            BaseInfo.BranchPartyNum = branchnnum
            BaseInfo.MobilePhone = phonenum
            BaseInfo.email = email
            BaseInfo.img =''
            try:
                BaseInfo.save()
            except:
                #TODO::保存时出现异常,需要进行处理
                return render(request,"userinformation_add.html")
                pass


        #get new_user
        new_user=None
        try:
            new_user=baseInfo.objects.get(name=name,MobilePhone=phonenum)
        except:
            print("用户基本信息插入出错，请检查")
            #TODO::这个地方，添加一个form,把这些数据在返回前端
            return render(request, "userinformation_add.html")
        # education

        edutype1 = request.POST.get("edutype1", "")
        school1 = request.POST.get("school1", "")
        major1 = request.POST.get("major1", "")
        edustartdate1 = request.POST.get("edustartdate1", "")
        eduenddate1 = request.POST.get("eduenddate1", "")
        eduexprience1 = request.POST.get("eduexprience1", "")
        degree1 = request.POST.get("degree1", "")

        edutype2 = request.POST.get("edutype2", "")
        school2 = request.POST.get("school2", "")
        major2 = request.POST.get("major2", "")
        edustartdate2 = request.POST.get("edustartdate2", "")
        eduenddate2 = request.POST.get("eduenddate2", "")
        eduexprience2 = request.POST.get("eduexprience2", "")
        degree2 = request.POST.get("degree2", "")

        if ((school1!='' and major1!='')):
            edu = education()
            edu.user = new_user
            edu.EduType = edutype1
            edu.college = school1
            edu.major = major1
            edu.ComeIntoSchoolDate = edustartdate1
            edu.GraduateDate = eduenddate1
            edu.EduExperience = eduexprience1
            edu.EduDegree = degree1
            edu.save()

            edu2 = education()
        if (not (school2 == '' and major2 == '')):
            edu2.user = new_user
            edu2.EduType = edutype2
            edu2.college = school2
            edu2.major = major2
            edu2.ComeIntoSchoolDate = edustartdate2
            edu2.GraduateDate = eduenddate2
            edu2.EduExperience = eduexprience2
            edu2.EduDegree = degree2
            edu2.save()

        # workunit
        workunit = request.POST.get("workunit", "")
        workunitaddr = request.POST.get("workunitaddr", "")
        familyaddr = request.POST.get("familyaddr", "")
        special = request.POST.get("special", "")
        workjob = request.POST.get("workjob", "")

        workphone = request.POST.get("workphone", "")
        familyphone = request.POST.get("familyphone", "")
        salary = request.POST.get("salary", "")
        workproperty = request.POST.get("workproperty", "")
        workaddremailnum = request.POST.get("workaddremailnum", "")

        familyaddremailnum = request.POST.get("familyaddremailnum", "")
        selectaddr = request.POST.get("selectaddr", "")

        if (not(workunit=='')):
            work = Work()
            work.user=new_user
            work.WorkUnit = workunit
            work.WorkUnitAddr = workunitaddr
            work.AdministrativeLevel = workjob
            work.WorkPhone = workphone
            work.WorkPostcode = workaddremailnum
            work.PropertyOfWorkUnit = workproperty
            work.HomeAddr = familyaddr
            work.HomePhone = familyphone
            work.HomePostcode= familyaddremailnum
            work.specialty = special
            work.ContactAddrType = selectaddr
            work.WelfareLevel = salary
            work.save()


        # position
        selectposition1 = request.POST.get("selectposition1", "")
        positionstartdate1 = request.POST.get("positionstartdate1", "")
        positionenddate1 = request.POST.get("positionenddate1", "")
        positionwhich1 = request.POST.get("positionwhich1", "")
        positionworkdetail1 = request.POST.get("positionworkdetail1", "")

        selectposition2 = request.POST.get("selectposition2", "")
        positionstartdate2 = request.POST.get("positionstartdate2", "")
        positionenddate2 = request.POST.get("positionenddate2", "")
        positionwhich2 = request.POST.get("positionwhich2", "")
        positionworkdetail2 = request.POST.get("positionworkdetail2", "")

        selectposition3 = request.POST.get("selectposition3", "")
        positionstartdate3 = request.POST.get("positionstartdate3", "")
        positionenddate3 = request.POST.get("positionenddate3", "")
        positionwhich3 = request.POST.get("positionwhich3", "")
        positionworkdetail3 = request.POST.get("positionworkdetail3", "")

        if (not(positionwhich1=='' and positionworkdetail1=='')):
            position1 = PositionSincePast()
            position1.user = new_user
            position1.WorkType = selectposition1
            position1.StartDate = positionstartdate1
            position1.EndDate = positionenddate1
            position1.department = positionworkdetail1
            position1.Which = positionwhich1
            position1.save()
        if (not (positionwhich2 == '' and positionworkdetail2 == '')):
            position2 = PositionSincePast()
            position2.user = new_user
            position2.WorkType = selectposition2
            position2.StartDate = positionstartdate2
            position2.EndDate = positionenddate2
            position2.department = positionworkdetail2
            position2.Which = positionwhich2
            position2.save()
        if (not (positionwhich3 == '' and positionworkdetail3 == '')):
            position3 = PositionSincePast()
            position3.user = new_user
            position3.WorkType = selectposition3
            position3.StartDate = positionstartdate3
            position3.EndDate = positionenddate3
            position3.department = positionworkdetail3
            position3.Which = positionwhich3
            position3.save()


        # resume
        resumestartdate1 = request.POST.get("resumestartdate1", "")
        resumeenddate1 = request.POST.get("resumeenddate1", "")
        resumepositiondetail1 = request.POST.get("resumepositiondetail1", "")

        resumestartdate2 = request.POST.get("resumestartdate2", "")
        resumeenddate2 = request.POST.get("resumeenddate2", "")
        resumepositiondetail2 = request.POST.get("resumepositiondetail2", "")

        resumestartdate3 = request.POST.get("resumestartdate3", "")
        resumeenddate3 = request.POST.get("resumeenddate3", "")
        resumepositiondetail3 = request.POST.get("resumepositiondetail3", "")

        resumestartdate4 = request.POST.get("resumestartdate4", "")
        resumeenddate4 = request.POST.get("resumeenddate4", "")
        resumepositiondetail4 = request.POST.get("resumepositiondetail4", "")

        resumestartdate5 = request.POST.get("resumestartdate5", "")
        resumeenddate5 = request.POST.get("resumeenddate5", "")
        resumepositiondetail5 = request.POST.get("resumepositiondetail5", "")

        if not(resumepositiondetail1==''):
            resume1 = Resume()
            resume1.user = new_user
            resume1.StartDate = resumestartdate1
            resume1.EndDate = resumeenddate1
            resume1.department = resumepositiondetail1
            resume1.save()
        if not (resumepositiondetail2 == ''):
            resume2 = Resume()
            resume2.user = new_user
            resume2.StartDate = resumestartdate2
            resume2.EndDate = resumeenddate2
            resume2.department = resumepositiondetail2
            resume2.save()
        if not (resumepositiondetail3 == ''):
            resume3 = Resume()
            resume3.user = new_user
            resume3.StartDate = resumestartdate3
            resume3.EndDate = resumeenddate3
            resume3.department = resumepositiondetail3
            resume3.save()
        if not (resumepositiondetail4 == ''):
            resume4 = Resume()
            resume4.user = new_user
            resume4.StartDate = resumestartdate4
            resume4.EndDate = resumeenddate4
            resume4.department = resumepositiondetail4
            resume4.save()
        if not (resumepositiondetail5 == ''):
            resume5 = Resume()
            resume5.user = new_user
            resume5.StartDate = resumestartdate5
            resume5.EndDate = resumeenddate5
            resume5.department = resumepositiondetail5
            resume5.save()

        # 奖励信息
        AwardTime1 = request.POST.get('AwardTime1', '')
        AwardGrade1 = request.POST.get('AwardGrade1', '')
        AwardUnit1 = request.POST.get('AwardUnit1', '')
        AwardDetail1 = request.POST.get('AwardDetail1', '')
        if (not (AwardUnit1 == '' and AwardDetail1 == '')):
            awardinfo = AwardInfo()
            awardinfo.AwardDate = AwardTime1
            awardinfo.AwardLevel = AwardGrade1
            awardinfo.HoldWorkUnit = AwardUnit1
            awardinfo.AwardDetail = AwardDetail1
            awardinfo.user = new_user
            awardinfo.save()

        AwardTime2 = request.POST.get('AwardTime2', '')
        AwardGrade2 = request.POST.get('AwardGrade2', '')
        AwardUnit2 = request.POST.get('AwardUnit2', '')
        AwardDetail2 = request.POST.get('AwardDetail2', '')
        if (not (AwardUnit2 == '' and AwardDetail2 == '')):
            awardinfo = AwardInfo()
            awardinfo.AwardDate = AwardTime2
            awardinfo.AwardLevel = AwardGrade2
            awardinfo.HoldWorkUnit = AwardUnit2
            awardinfo.AwardDetail = AwardDetail2
            awardinfo.user = new_user
            awardinfo.save()

        AwardTime3 = request.POST.get('AwardTime3', '')
        AwardGrade3 = request.POST.get('AwardGrade3', '')
        AwardUnit3 = request.POST.get('AwardUnit3', '')
        AwardDetail3 = request.POST.get('AwardDetail3', '')
        if (not (AwardUnit3 == '' and AwardDetail3 == '')):
            awardinfo = AwardInfo()
            awardinfo.AwardDate = AwardTime3
            awardinfo.AwardLevel = AwardGrade3
            awardinfo.HoldWorkUnit = AwardUnit3
            awardinfo.AwardDetail = AwardDetail3
            awardinfo.user = new_user
            awardinfo.save()



        # 处罚
        punishDetails1 = request.POST.get('punishDetails1', '')
        punishDate1 = request.POST.get('punishDate1', '')
        CancelDetail1 = request.POST.get('CancelDetail1', '')
        if (not (punishDetails1 == '' and CancelDetail1 == '')):
            punish = Punish()
            punish.PunishDate = punishDate1
            punish.details = punishDetails1
            punish.CancelDetail = CancelDetail1
            punish.user = new_user
            punish.save()

        punishDetails2 = request.POST.get('punishDetails2', '')
        punishDate2 = request.POST.get('punishDate2', '')
        CancelDetail2 = request.POST.get('CancelDetail2', '')
        if (not (punishDetails2 == '' and CancelDetail2 == '')):
            punish = Punish()
            punish.PunishDate = punishDate2
            punish.details = punishDetails2
            punish.CancelDetail = CancelDetail2
            punish.user = new_user
            punish.save()

        # 参与活动
        activityName1 = request.POST.get("activityName1", '')
        addr1 = request.POST.get("addr1", '')
        introducer1 = request.POST.get("introducer1", '')
        Position1 = request.POST.get('Position1', '')
        startDate1 = request.POST.get('startDate1', '')

        Activity_IsLinkedNow1 = request.POST.get('Activity_IsLinkedNow1', '')

        if (not (activityName1 == '' and addr1 == '' and Position1 == '' and startDate1 == '')):
            newacitivity = activity()
            newacitivity.user = new_user
            newacitivity.StartDate = startDate1
            newacitivity.ActivityName = activityName1
            newacitivity.addr = addr1
            newacitivity.introducer = introducer1
            newacitivity.PositionOfIntroducer = Position1
            newacitivity.IsLinkedNow = Activity_IsLinkedNow1
            newacitivity.save()

        activityName2 = request.POST.get("activityName2", '')
        addr2 = request.POST.get("addr2", '')
        introducer2 = request.POST.get("introducer2", '')
        Position2 = request.POST.get('Position2', '')
        startDate2 = request.POST.get('startDate2', '')

        Activity_IsLinkedNow2 = request.POST.get('Activity_IsLinkedNow2', '')

        if (not (activityName2 == '' and addr2 == '' and Position2 == '' and startDate2 == '')):
            position = activity()
            position.user = new_user
            position.StartDate = startDate2
            position.ActivityName = activityName2
            position.addr = addr2
            position.introducer = introducer2
            position.PositionOfIntroducer = Position2
            position.IsLinkedNow = Activity_IsLinkedNow2
            position.save()

        activityName3 = request.POST.get("activityName3", '')
        addr3 = request.POST.get("addr3", '')
        introducer3 = request.POST.get("introducer3", '')
        Position3 = request.POST.get('Position3', '')
        startDate3 = request.POST.get('startDate3', '')

        Activity_IsLinkedNow3 = request.POST.get('Activity_IsLinkedNow3', '')

        if (not (activityName3 == '' and addr3 == '' and Position3 == '' and startDate3 == '')):
            position = activity()
            position.user = new_user
            position.StartDate = startDate3
            position.ActivityName = activityName3
            position.addr = addr3
            position.introducer = introducer3
            position.PositionOfIntroducer = Position3
            position.IsLinkedNow = Activity_IsLinkedNow3
            position.save()
        # 家庭成员
        memberName1 = request.POST.get("memberName1", '')
        memrelation1 = request.POST.get("memrelation1", '')
        memBornDate1 = request.POST.get("memBornDate1", '')
        EduLevel1 = request.POST.get("EduLevel1", '')
        memPoliticalIdentity1 = request.POST.get('memPoliticalIdentity1', '')
        memDepartmentPosition1 = request.POST.get('memDepartmentPosition1', '')

        if (not (memberName1 == '' and memrelation1 == '')):
            familymember = FamilyMember()
            familymember.name = memberName1
            familymember.user = new_user
            familymember.relation = memrelation1
            familymember.BornDate = memBornDate1
            familymember.EducationLevel = EduLevel1
            familymember.PoliticalIdentity = memPoliticalIdentity1
            familymember.DepartmentPosition = memDepartmentPosition1
            familymember.save()

        memberName2 = request.POST.get("memberName2", '')
        memrelation2 = request.POST.get("memrelation2", '')
        memBornDate2 = request.POST.get("memBornDate2", '')
        EduLevel2 = request.POST.get("EduLevel2", '')
        memPoliticalIdentity2 = request.POST.get('memPoliticalIdentity2', '')
        memDepartmentPosition2 = request.POST.get('memDepartmentPosition2', '')

        if (not (memberName2 == '' and memrelation2 == '')):
            familymember = FamilyMember()
            familymember.name = memberName2
            familymember.user = new_user
            familymember.relation = memrelation2
            familymember.BornDate = memBornDate2
            familymember.EducationLevel = EduLevel2
            familymember.PoliticalIdentity = memPoliticalIdentity2
            familymember.DepartmentPosition = memDepartmentPosition2
            familymember.save()

        memberName3 = request.POST.get("memberName3", '')
        memrelation3 = request.POST.get("memrelation3", '')
        memBornDate3 = request.POST.get("memBornDate3", '')
        EduLevel3 = request.POST.get("EduLevel3", '')
        memPoliticalIdentity3 = request.POST.get('memPoliticalIdentity3', '')
        memDepartmentPosition3 = request.POST.get('memDepartmentPosition3', '')

        if (not (memberName3 == '' and memrelation3 == '')):
            familymember = FamilyMember()
            familymember.name = memberName3
            familymember.user = new_user
            familymember.relation = memrelation3
            familymember.BornDate = memBornDate3
            familymember.EducationLevel = EduLevel3
            familymember.PoliticalIdentity = memPoliticalIdentity3
            familymember.DepartmentPosition = memDepartmentPosition3
            familymember.save()

        memberName4 = request.POST.get("memberName4", '')
        memrelation4 = request.POST.get("memrelation4", '')
        memBornDate4 = request.POST.get("memBornDate4", '')
        EduLevel4 = request.POST.get("EduLevel4", '')
        memPoliticalIdentity4 = request.POST.get('memPoliticalIdentity4', '')
        memDepartmentPosition4 = request.POST.get('memDepartmentPosition4', '')

        if (not (memberName4 == '' and memrelation4 == '')):
            familymember = FamilyMember()
            familymember.name = memberName4
            familymember.user = new_user
            familymember.relation = memrelation4
            familymember.BornDate = memBornDate4
            familymember.EducationLevel = EduLevel4
            familymember.PoliticalIdentity = memPoliticalIdentity4
            familymember.DepartmentPosition = memDepartmentPosition4
            familymember.save()

        memberName5 = request.POST.get("memberName5", '')
        memrelation5 = request.POST.get("memrelation5", '')
        memBornDate5 = request.POST.get("memBornDate5", '')
        EduLevel5 = request.POST.get("EduLevel5", '')
        memPoliticalIdentity5 = request.POST.get('memPoliticalIdentity5', '')
        memDepartmentPosition5 = request.POST.get('memDepartmentPosition5', '')

        if (not (memberName5 == '' and memrelation5 == '')):
            familymember = FamilyMember()
            familymember.name = memberName5
            familymember.user = new_user
            familymember.relation = memrelation5
            familymember.BornDate = memBornDate5
            familymember.EducationLevel = EduLevel5
            familymember.PoliticalIdentity = memPoliticalIdentity5
            familymember.DepartmentPosition = memDepartmentPosition5
            familymember.save()

        memberName6 = request.POST.get("memberName6", '')
        memrelation6 = request.POST.get("memrelation6", '')
        memBornDate6 = request.POST.get("memBornDate6", '')
        EduLevel6 = request.POST.get("EduLevel6", '')
        memPoliticalIdentity6 = request.POST.get('memPoliticalIdentity6', '')
        memDepartmentPosition6 = request.POST.get('memDepartmentPosition6', '')

        if (not (memberName6 == '' and memrelation6 == '')):
            familymember = FamilyMember()
            familymember.name = memberName6
            familymember.user = new_user
            familymember.relation = memrelation6
            familymember.BornDate = memBornDate6
            familymember.EducationLevel = EduLevel6
            familymember.PoliticalIdentity = memPoliticalIdentity6
            familymember.DepartmentPosition = memDepartmentPosition6
            familymember.save()
        # 民革关系
        relation1 = request.POST.get("relation1", '')
        relationName1 = request.POST.get("relationName1", '')
        BornDate1 = request.POST.get("BornDate1", '')
        EducationLevel1 = request.POST.get("EducationLevel1", '')
        PoliticalIdentity1 = request.POST.get("PoliticalIdentity1", '')
        DepartmentPosition1 = request.POST.get("DepartmentPosition1", '')
        IsLinkedNow1 = request.POST.get('IsLinkedNow1', '')

        if (not (relationName1 == '' and relation1 == '')):
            mingeRelation = MinGeRelation()
            mingeRelation.BornDate = BornDate1
            mingeRelation.relation = relation1
            mingeRelation.name = relationName1
            mingeRelation.user = new_user
            mingeRelation.EducationLevel = EducationLevel1
            mingeRelation.PoliticalIdentity = PoliticalIdentity1
            mingeRelation.DepartmentPosition = DepartmentPosition1
            mingeRelation.IsLinkedNow = IsLinkedNow1
            mingeRelation.save()

        relation2 = request.POST.get("relation2", '')
        relationName2 = request.POST.get("relationName2", '')
        BornDate2 = request.POST.get("BornDate2", '')
        EducationLevel2 = request.POST.get("EducationLevel2", '')
        PoliticalIdentity2 = request.POST.get("PoliticalIdentity2", '')
        DepartmentPosition2 = request.POST.get("DepartmentPosition2", '')
        IsLinkedNow2 = request.POST.get('IsLinkedNow2', '')


        if (not (relationName2 == '' and relation2 == '')):
            mingeRelation = MinGeRelation()
            mingeRelation.BornDate = BornDate2
            mingeRelation.relation = relation2
            mingeRelation.name = relationName2
            mingeRelation.user = new_user
            mingeRelation.EducationLevel = EducationLevel2
            mingeRelation.PoliticalIdentity = PoliticalIdentity2
            mingeRelation.DepartmentPosition = DepartmentPosition2
            mingeRelation.IsLinkedNow = IsLinkedNow2
            mingeRelation.save()

        relation3 = request.POST.get("relation3", '')
        relationName3 = request.POST.get("relationName3", '')
        BornDate3 = request.POST.get("BornDate3", '')
        EducationLevel3 = request.POST.get("EducationLevel3", '')
        PoliticalIdentity3 = request.POST.get("PoliticalIdentity3", '')
        DepartmentPosition3 = request.POST.get("DepartmentPosition3", '')
        IsLinkedNow3 = request.POST.get('IsLinkedNow3', '')

        if (not (relationName3 == '' and relation3 == '')):
            mingeRelation = MinGeRelation()
            mingeRelation.BornDate = BornDate3
            mingeRelation.relation = relation3
            mingeRelation.name = relationName3
            mingeRelation.user = new_user
            mingeRelation.EducationLevel = EducationLevel3
            mingeRelation.PoliticalIdentity = PoliticalIdentity3
            mingeRelation.DepartmentPosition = DepartmentPosition3
            mingeRelation.IsLinkedNow = IsLinkedNow3
            mingeRelation.save()

        relation4 = request.POST.get("relation4", '')
        relationName4 = request.POST.get("relationName4", '')
        BornDate4 = request.POST.get("BornDate4", '')
        EducationLevel4 = request.POST.get("EducationLevel4", '')
        PoliticalIdentity4 = request.POST.get("PoliticalIdentity4", '')
        DepartmentPosition4 = request.POST.get("DepartmentPosition4", '')
        IsLinkedNow4 = request.POST.get('IsLinkedNow4', '')

        if (not (relationName4 == '' and relation4 == '')):
            mingeRelation = MinGeRelation()
            mingeRelation.BornDate = BornDate4
            mingeRelation.relation = relation4
            mingeRelation.name = relationName4
            mingeRelation.user = new_user
            mingeRelation.EducationLevel = EducationLevel4
            mingeRelation.PoliticalIdentity = PoliticalIdentity4
            mingeRelation.DepartmentPosition = DepartmentPosition4
            mingeRelation.IsLinkedNow = IsLinkedNow4
            mingeRelation.save()
        relation5 = request.POST.get("relation5", '')
        relationName5 = request.POST.get("relationName5", '')
        BornDate5 = request.POST.get("BornDate5", '')
        EducationLevel5 = request.POST.get("EducationLevel5", '')
        PoliticalIdentity5 = request.POST.get("PoliticalIdentity5", '')
        DepartmentPosition5 = request.POST.get("DepartmentPosition5", '')
        IsLinkedNow5 = request.POST.get('IsLinkedNow5', '')

        if (not (relationName5 == '' and relation5 == '')):
            mingeRelation = MinGeRelation()
            mingeRelation.BornDate = BornDate5
            mingeRelation.relation = relation5
            mingeRelation.name = relationName5
            mingeRelation.user = new_user
            mingeRelation.EducationLevel = EducationLevel5
            mingeRelation.PoliticalIdentity = PoliticalIdentity5
            mingeRelation.DepartmentPosition = DepartmentPosition5
            mingeRelation.IsLinkedNow = IsLinkedNow5
            mingeRelation.save()
        # 添加到通讯录
        add_contact = ContactList()
        add_contact.name = name
        add_contact.MobilePhone = phonenum
        # add_contact.qqNum =
        # add_contact.gender = models.CharField(max_length=255, verbose_name=u"性别")
        add_contact.BornDate = borndate
        add_contact.nation = nation
        # add_contact.EduExperience =
        # add_contact.PropertyOfWorkUnit = models.CharField(max_length=100, verbose_name=u"教育经历")
        add_contact.WorkUnit = workunit
        # add_contact.DateComeIntoMinGe = models.DateField(verbose_name=u"加入日期")
        if branchnnum=='':
            branchnnum='0'
        add_contact.BranchPartyName = ConfigInfo.setlist[int(branchnnum)-1]
        add_contact.save()

        return render(request, "userinformation.html", {
            "Msg": "请修改页面后保存",
            "userinfo": new_user
        })
class DeleteInfo(View):
    def get(self,request):
        userID=request.GET.get('id', '-1')
        if userID=='':
            return render(request, "userinformation_add.html",{"user": request.user, "time": datetime.now()})
        userID=int(userID)
        userToDelete=None
        try:
            userToDelete=baseInfo.objects.get(id=userID)
        except:
            return render(request, "userinformation_add.html", {
                "Msg":"删除用户失败，没有这个用户"
            })
        try:
            contactToDelete=ContactList.objects.get(name=userToDelete.name)
        except:
            return render(request, "userinformation_add.html", {
                "Msg":"删除用户失败，没有这个用户"
            })

        userToDelete.delete()
        contactToDelete.delete()
        return render(request, "userinformation_add.html", {
            "Msg": "删除成功"
        })
class ModifyInfo(View):
    def get(self,request):
        if not request.user.is_authenticated():
            return render(request, "login.html",{"user": request.user, "time": datetime.now()})
        if not request.user.is_manager:
            return render(request, "login.html",{"user": request.user, "time": datetime.now()})
        userID = request.GET.get('name', '0')
        if userID == '' or userID=='0':
            return redirect('/userlist')
        userDis=None
        try:
            userDis=baseInfo.objects.get(name=userID)
        except:
            return render(request, "userinformation_add.html", {
                "Msg":"读取用户失败，没有这个用户",
            })
        return render(request, "userinformation_modify.html", {
            "Msg": "请修改页面后保存",
            "user":userDis,
            "new_user_id":userDis.id

        })
    def post(self,request):
        # baseinfo表
        if not request.user.is_authenticated():
            return render(request, "login.html")
        if not request.user.is_manager:
            return render(request, "login.html")
        name = request.POST.get("name", " ")
        nation = request.POST.get("selectnation", " ")
        Bornplace = request.POST.get("Bornplace", " ")

        #photo=request.FILES["photo"]
        partynum = request.POST.get("partynum", " ")
        phonenum = request.POST.get("phonenum", " ")

        nameused = request.POST.get("nameused", "")
        nativeplace = request.POST.get("nativeplace", "")
        borndate = request.POST.get("borndate", "")
        # 转换成日期对象
        borndate=ConfigInfo.getCorrectDate(borndate)
        branchname = request.POST.get("branchname", "")
        email = request.POST.get("email", "")

        religious = request.POST.get("religious", "")
        IDnum = request.POST.get("IDnum", "")
        branchnnum = request.POST.get("branchnnum", "")
        new_user=None
        try:
            new_user=baseInfo.objects.get(name=name)
        except:
            return render(request, "userinformation_modify.html", {
                "Msg": "读取用户失败，没有这个用户",
            })


        if (not (name == '' and IDnum == '' and phonenum == '')):
            BaseInfo = new_user

            BaseInfo.name = name
            BaseInfo.nameUsed = nameused
            BaseInfo.nation = nation
            BaseInfo.NativePlace = nativeplace

            BaseInfo.religious = religious
            BaseInfo.BornPlace = Bornplace
            BaseInfo.BornDate = borndate
            BaseInfo.IDCardNum = IDnum
            BaseInfo.PartyDocuNum = partynum

            BaseInfo.BranchParty = branchname
            BaseInfo.BranchPartyNum = branchnnum
            BaseInfo.MobilePhone = phonenum
            BaseInfo.email = email
            BaseInfo.img = ''
            BaseInfo.save()
            #try:
            #    BaseInfo.save()
            #except:
            #    # TODO::保存时出现异常,需要进行处理
            #    return render(request, "userinformation_add.html")
            #    pass

        # get new_user


        # education



        #edutype2 = request.POST.get("edutype2", "")
        #school2 = request.POST.get("school2", "")
        #major2 = request.POST.get("major2", "")
        #edustartdate2 = request.POST.get("edustartdate2", "")
        #edustartdate2 = ConfigInfo.getCorrectDate(edustartdate2)
        #eduenddate2 = request.POST.get("eduenddate2", "")
        #eduenddate2 = ConfigInfo.getCorrectDate(eduenddate2)
        #eduexprience2 = request.POST.get("eduexprience2", "")
        #degree2 = request.POST.get("degree2", "")
        #再保存之前获取所有的对象，保存后就删除。
        for count in range(0,3):
            eduid=request.POST.get("Eduid"+str(count), "")
            edutype1 = request.POST.get("edutype"+str(count), "")
            school1 = request.POST.get("school"+str(count), "")
            major1 = request.POST.get("major"+str(count), "")
            edustartdate1 = request.POST.get("edustartdate"+str(count), "")
            edustartdate1 = ConfigInfo.getCorrectDate(edustartdate1)
            eduenddate1 = request.POST.get("eduenddate"+str(count), "")
            eduenddate1 = ConfigInfo.getCorrectDate(eduenddate1)
            eduexprience1 = request.POST.get("eduexprience"+str(count), "")
            degree1 = request.POST.get("degree"+str(count), "")


            if ((school1!='' and major1!='')):
                edu=None
                try:
                    edu=education.objects.get(id=int(eduid))
                except:
                    edu=education()
                edu.user = new_user
                edu.EduType = edutype1
                edu.college = school1
                edu.major = major1
                edu.ComeIntoSchoolDate = edustartdate1
                edu.GraduateDate = eduenddate1
                edu.EduExperience = eduexprience1
                edu.EduDegree = degree1
                edu.save()



        #if (not (school2 == '' and major2 == '')):
        #    edu2 = education()
        #    edu2.user = new_user
        #    edu2.EduType = edutype2
        #    edu2.college = school2
        #    edu2.major = major2
        #    edu2.ComeIntoSchoolDate = edustartdate2
        #    edu2.GraduateDate = eduenddate2
        #    edu2.EduExperience = eduexprience2
        #    edu2.EduDegree = degree2
        #    edu2.save()
        #    if len(alledu) > 2:
        #        alledu[1].delete()

        # workunit
        workunitid= request.POST.get("workunitid1", "")
        workunit = request.POST.get("workunit", "")
        workunitaddr = request.POST.get("workunitaddr", "")
        familyaddr = request.POST.get("familyaddr", "")
        special = request.POST.get("special", "")
        workjob = request.POST.get("workjob", "")

        workphone = request.POST.get("workphone", "")
        familyphone = request.POST.get("familyphone", "")
        salary = request.POST.get("WelfareLevel", "")
        workproperty = request.POST.get("workproperty", "")
        workaddremailnum = request.POST.get("workaddremailnum", "")

        familyaddremailnum = request.POST.get("familyaddremailnum", "")
        selectaddr = request.POST.get("selectaddr", "")

        if (not (workunit == '')):
            work = None
            try:
                work = Work.objects.get(id=int(workunitid))
            except:
                work=Work()

            work.user = new_user
            work.WorkUnit = workunit
            work.WorkUnitAddr = workunitaddr
            work.AdministrativeLevel = workjob
            work.WorkPhone = workphone
            work.WorkPostcode = workaddremailnum
            work.PropertyOfWorkUnit = workproperty
            work.HomeAddr = familyaddr
            work.HomePhone = familyphone
            work.HomePostcode = familyaddremailnum
            work.specialty = special
            work.ContactAddrType = selectaddr
            work.WelfareLevel = salary
            work.save()


        # position
        for count in range(0, 4):
            positionid= request.POST.get("positionid"+str(count), "")
            selectposition1 = request.POST.get("selectposition"+str(count), "")
            positionstartdate1 = request.POST.get("positionstartdate"+str(count), "")
            positionstartdate1= ConfigInfo.getCorrectDate(positionstartdate1)
            positionenddate1 = request.POST.get("positionenddate"+str(count), "")
            positionenddate1 = ConfigInfo.getCorrectDate(positionenddate1)
            positionwhich1 = request.POST.get("positionwhich"+str(count), "")
            positionworkdetail1 = request.POST.get("positionworkdetail"+str(count), "")

        #selectposition2 = request.POST.get("selectposition2", "")
        #positionstartdate2 = request.POST.get("positionstartdate2", "")
        #positionstartdate2 = ConfigInfo.getCorrectDate(positionstartdate2)
        #positionenddate2 = request.POST.get("positionenddate2", "")
        #positionenddate2 = ConfigInfo.getCorrectDate(positionenddate2)
        #positionwhich2 = request.POST.get("positionwhich2", "")
        #positionworkdetail2 = request.POST.get("positionworkdetail2", "")
#
        #selectposition3 = request.POST.get("selectposition3", "")
        #positionstartdate3 = request.POST.get("positionstartdate3", "")
        #positionstartdate3 = ConfigInfo.getCorrectDate(positionstartdate3)
        #positionenddate3 = request.POST.get("positionenddate3", "")
        #positionenddate3 = ConfigInfo.getCorrectDate(positionenddate3)
        #positionwhich3 = request.POST.get("positionwhich3", "")
        #positionworkdetail3 = request.POST.get("positionworkdetail3", "")
        #allposition=new_user.positionsincepast_set.all()
            if (not (positionwhich1 == '' and positionworkdetail1 == '')):
                position1 = None
                try:
                    position1 = PositionSincePast.objects.get(id=int(positionid))
                except:
                    position1 = PositionSincePast()
                position1.user = new_user
                position1.WorkType = selectposition1
                position1.StartDate = positionstartdate1
                position1.EndDate = positionenddate1
                position1.department = positionworkdetail1
                position1.Which = positionwhich1
                position1.save()


        #if (not (positionwhich2 == '' and positionworkdetail2 == '')):
        #    position2 = PositionSincePast()
        #    position2.user = new_user
        #    position2.WorkType = selectposition2
        #    position2.StartDate = positionstartdate2
        #    position2.EndDate = positionenddate2
        #    position2.department = positionworkdetail2
        #    position2.Which = positionwhich2
        #    position2.save()
        #    if len(allposition) >2:
        #        allposition[1].delete()
        #if (not (positionwhich3 == '' and positionworkdetail3 == '')):
        #    position3 = PositionSincePast()
        #    position3.user = new_user
        #    position3.WorkType = selectposition3
        #    position3.StartDate = positionstartdate3
        #    position3.EndDate = positionenddate3
        #    position3.department = positionworkdetail3
        #    position3.Which = positionwhich3
        #    position3.save()
        #    if len(allposition) >2:
        #        allposition[2].delete()

        # resume
        for count in range(0, 6):
            resumeid=request.POST.get("resumeid"+str(count), "")
            resumestartdate1 = request.POST.get("resumestartdate"+str(count), "")
            resumestartdate1=ConfigInfo.getCorrectDate(resumestartdate1)
            resumeenddate1 = request.POST.get("resumeenddate"+str(count), "")
            resumeenddate1 = ConfigInfo.getCorrectDate(resumeenddate1)
            resumepositiondetail1 = request.POST.get("resumepositiondetail"+str(count), "")
            if not (resumepositiondetail1 == ''):

              resume1 = None
              try:
                  resume1 = Resume.objects.get(id=int(resumeid))
              except:
                  resume1 = Resume()
              resume1.user = new_user
              resume1.StartDate = resumestartdate1
              resume1.EndDate = resumeenddate1
              resume1.department = resumepositiondetail1
              resume1.save()
        #resumestartdate2 = request.POST.get("resumestartdate2", "")
        #resumestartdate2 = ConfigInfo.getCorrectDate(resumestartdate2)
        #resumeenddate2 = request.POST.get("resumeenddate2", "")
        #resumeenddate2 = ConfigInfo.getCorrectDate(resumeenddate2)
        #resumepositiondetail2 = request.POST.get("resumepositiondetail2", "")

        #resumestartdate3 = request.POST.get("resumestartdate3", "")
        #resumestartdate3 = ConfigInfo.getCorrectDate(resumestartdate3)
        #resumeenddate3 = request.POST.get("resumeenddate3", "")
        #resumeenddate3 = ConfigInfo.getCorrectDate(resumeenddate3)
        #resumepositiondetail3 = request.POST.get("resumepositiondetail3", "")

        #resumestartdate4 = request.POST.get("resumestartdate4", "")
        #resumestartdate4 = ConfigInfo.getCorrectDate(resumestartdate4)
        #resumeenddate4 = request.POST.get("resumeenddate4", "")
        #resumeenddate4 = ConfigInfo.getCorrectDate(resumeenddate4)
        #resumepositiondetail4 = request.POST.get("resumepositiondetail4", "")

        #resumestartdate5 = request.POST.get("resumestartdate5", "")
        #resumestartdate5 = ConfigInfo.getCorrectDate(resumestartdate5)
        #resumeenddate5 = request.POST.get("resumeenddate5", "")
        #resumeenddate5 = ConfigInfo.getCorrectDate(resumeenddate5)
        #resumepositiondetail5 = request.POST.get("resumepositiondetail5", "")

        #if not (resumepositiondetail1 == ''):
        #    resume1 = Resume()
        #    resume1.user = new_user
        #    resume1.StartDate = resumestartdate1
        #    resume1.EndDate = resumeenddate1
        #    resume1.department = resumepositiondetail1
        #    resume1.save()
        #if not (resumepositiondetail2 == ''):
        #    resume2 = Resume()
        #    resume2.user = new_user
        #    resume2.StartDate = resumestartdate2
        #    resume2.EndDate = resumeenddate2
        #    resume2.department = resumepositiondetail2
        #    resume2.save()
        #if not (resumepositiondetail3 == ''):
        #    resume3 = Resume()
        #    resume3.user = new_user
        #    resume3.StartDate = resumestartdate3
        #    resume3.EndDate = resumeenddate3
        #    resume3.department = resumepositiondetail3
        #    resume3.save()
        #if not (resumepositiondetail4 == ''):
        #    resume4 = Resume()
        #    resume4.user = new_user
        #    resume4.StartDate = resumestartdate4
        #    resume4.EndDate = resumeenddate4
        #    resume4.department = resumepositiondetail4
        #    resume4.save()
        #if not (resumepositiondetail5 == ''):
        #    resume5 = Resume()
        #    resume5.user = new_user
        #    resume5.StartDate = resumestartdate5
        #    resume5.EndDate = resumeenddate5
        #    resume5.department = resumepositiondetail5
        #    resume5.save()

            # 奖励信息
        for count in range(0,3):
            awardid=request.POST.get('Awardid'+str(count), '')
            AwardTime1 = request.POST.get('AwardTime'+str(count), '')
            AwardTime1=ConfigInfo.getCorrectDate(AwardTime1)
            AwardGrade1 = request.POST.get('AwardGrade'+str(count), '')
            AwardUnit1 = request.POST.get('AwardUnit'+str(count), '')
            AwardDetail1 = request.POST.get('AwardDetail'+str(count), '')
            if (not (AwardUnit1 == '' and AwardDetail1 == '')):
                awardinfo = None
                try:
                    awardinfo = AwardInfo.objects.get(id=int(awardid))
                except:
                    awardinfo = AwardInfo()
                awardinfo.AwardDate = AwardTime1
                awardinfo.AwardLevel = AwardGrade1
                awardinfo.HoldWorkUnit = AwardUnit1
                awardinfo.AwardDetail = AwardDetail1
                awardinfo.user = new_user
                awardinfo.save()



        # 处罚
        for count in range(0,3):
            punishid= request.POST.get('punishid'+str(count), '')
            punishDetails1 = request.POST.get('punishDetails'+str(count), '')
            punishDate1 = request.POST.get('punishDate'+str(count), '')
            punishDate1 = ConfigInfo.getCorrectDate(punishDate1)
            CancelDetail1 = request.POST.get('CancelDetail'+str(count), '')
            if (not (punishDetails1 == '' and CancelDetail1 == '')):
                punish = None
                try:
                    punish = Punish.objects.get(id=int(punishid))
                except:
                    punish = Punish()
                punish.PunishDate = punishDate1
                punish.details = punishDetails1
                punish.CancelDetail = CancelDetail1
                punish.user = new_user
                punish.save()

        #punishDetails2 = request.POST.get('punishDetails2', '')
        #punishDate2 = request.POST.get('punishDate2', '')
        #CancelDetail2 = request.POST.get('CancelDetail2', '')
        #if (not (punishDetails2 == '' and CancelDetail2 == '')):
        #    punish = Punish()
        #    punish.PunishDate = punishDate2
        #    punish.details = punishDetails2
        #    punish.CancelDetail = CancelDetail2
        #    punish.user = new_user
        #    punish.save()

        # 参与活动
        for count in range(0, 4):
            activityid=request.POST.get("activityid"+str(count), '')
            activityName1 = request.POST.get("activityName"+str(count), '')
            addr1 = request.POST.get("addr"+str(count), '')
            introducer1 = request.POST.get("introducer"+str(count), '')
            Position1 = request.POST.get('Position'+str(count), '')
            startDate1 = request.POST.get('startDate'+str(count), '')
            startDate1=ConfigInfo.getCorrectDate(startDate1)

            Activity_IsLinkedNow1 = request.POST.get('Activity_IsLinkedNow'+str(count), '')

            if (not (activityName1 == '' and addr1 == '' and Position1 == '' )):
                newacitivity = None
                try:
                    newacitivity = activity.objects.get(id=int(activityid))
                except:
                    newacitivity = activity()
                newacitivity.user = new_user
                newacitivity.StartDate = startDate1
                newacitivity.ActivityName= activityName1
                newacitivity.addr = addr1
                newacitivity.introducer = introducer1
                newacitivity.PositionOfIntroducer = Position1
                newacitivity.IsLinkedNow = Activity_IsLinkedNow1
                newacitivity.save()

        #activityName2 = request.POST.get("activityName2", '')
        #addr2 = request.POST.get("addr2", '')
        #introducer2 = request.POST.get("introducer2", '')
        #Position2 = request.POST.get('Position2', '')
        #startDate2 = request.POST.get('startDate2', '')
#
        #Activity_IsLinkedNow2 = request.POST.get('Activity_IsLinkedNow2', '')
#
        #if (not (activityName2 == '' and addr2 == '' and Position2 == '' and startDate2 == '')):
        #    position = activity()
        #    position.user = new_user
        #    position.StartDate = startDate2
        #    position.AcitivityName = activityName2
        #    position.addr = addr2
        #    position.introducer = introducer2
        #    position.PositionOfIntroducer = Position2
        #    position.IsLinkedNow = Activity_IsLinkedNow2
        #    position.save()
#
        #activityName3 = request.POST.get("activityName3", '')
        #addr3 = request.POST.get("addr3", '')
        #introducer3 = request.POST.get("introducer3", '')
        #Position3 = request.POST.get('Position3', '')
        #startDate3 = request.POST.get('startDate3', '')
#
        #Activity_IsLinkedNow3 = request.POST.get('Activity_IsLinkedNow3', '')
#
        #if (not (activityName3 == '' and addr3 == '' and Position3 == '' and startDate3 == '')):
        #    position = activity()
        #    position.user = new_user
        #    position.StartDate = startDate3
        #    position.AcitivityName = activityName3
        #    position.addr = addr3
        #    position.introducer = introducer3
        #    position.PositionOfIntroducer = Position3
        #    position.IsLinkedNow = Activity_IsLinkedNow3
        #    position.save()


        # 家庭成员
        for count in range(0, 7):
            memberid=request.POST.get("memberid"+str(count), '')
            memberName1 = request.POST.get("memberName"+str(count), '')
            memrelation1 = request.POST.get("memrelation"+str(count), '')
            memBornDate1 = request.POST.get("memBornDate"+str(count), '')
            memBornDate1=ConfigInfo.getCorrectDate(memBornDate1)
            EduLevel1 = request.POST.get("EduLevel"+str(count), '')
            memPoliticalIdentity1 = request.POST.get('memPoliticalIdentity'+str(count), '')
            memDepartmentPosition1 = request.POST.get('memDepartmentPosition'+str(count), '')

            if (not (memberName1 == '' and memrelation1 == '')):
                familymember = None
                try:
                    familymember = FamilyMember.objects.get(id=int(memberid))
                except:
                    familymember = FamilyMember()
                familymember.name = memberName1
                familymember.user = new_user
                familymember.relation = memrelation1
                familymember.BornDate = memBornDate1
                familymember.EducationLevel = EduLevel1
                familymember.PoliticalIdentity = memPoliticalIdentity1
                familymember.DepartmentPosition = memDepartmentPosition1
                familymember.save()

        #memberName2 = request.POST.get("memberName2", '')
        #memrelation2 = request.POST.get("memrelation2", '')
        #memBornDate2 = request.POST.get("memBornDate2", '')
        #EduLevel2 = request.POST.get("EduLevel2", '')
        #memPoliticalIdentity2 = request.POST.get('memPoliticalIdentity2', '')
        #memDepartmentPosition2 = request.POST.get('memDepartmentPosition2', '')
#
        #if (not (memberName2 == '' and memrelation2 == '')):
        #    familymember = FamilyMember()
        #    familymember.name = memberName2
        #    familymember.user = new_user
        #    familymember.relation = memrelation2
        #    familymember.BornDate = memBornDate2
        #    familymember.EducationLevel = EduLevel2
        #    familymember.PoliticalIdentity = memPoliticalIdentity2
        #    familymember.DepartmentPosition = memDepartmentPosition2
        #    familymember.save()
#
        #memberName3 = request.POST.get("memberName3", '')
        #memrelation3 = request.POST.get("memrelation3", '')
        #memBornDate3 = request.POST.get("memBornDate3", '')
        #EduLevel3 = request.POST.get("EduLevel3", '')
        #memPoliticalIdentity3 = request.POST.get('memPoliticalIdentity3', '')
        #memDepartmentPosition3 = request.POST.get('memDepartmentPosition3', '')
#
        #if (not (memberName3 == '' and memrelation3 == '')):
        #    familymember = FamilyMember()
        #    familymember.name = memberName3
        #    familymember.user = new_user
        #    familymember.relation = memrelation3
        #    familymember.BornDate = memBornDate3
        #    familymember.EducationLevel = EduLevel3
        #    familymember.PoliticalIdentity = memPoliticalIdentity3
        #    familymember.DepartmentPosition = memDepartmentPosition3
        #    familymember.save()
#
        #memberName4 = request.POST.get("memberName4", '')
        #memrelation4 = request.POST.get("memrelation4", '')
        #memBornDate4 = request.POST.get("memBornDate4", '')
        #EduLevel4 = request.POST.get("EduLevel4", '')
        #memPoliticalIdentity4 = request.POST.get('memPoliticalIdentity4', '')
        #memDepartmentPosition4 = request.POST.get('memDepartmentPosition4', '')
#
        #if (not (memberName4 == '' and memrelation4 == '')):
        #    familymember = FamilyMember()
        #    familymember.name = memberName4
        #    familymember.user = new_user
        #    familymember.relation = memrelation4
        #    familymember.BornDate = memBornDate4
        #    familymember.EducationLevel = EduLevel4
        #    familymember.PoliticalIdentity = memPoliticalIdentity4
        #    familymember.DepartmentPosition = memDepartmentPosition4
        #    familymember.save()
#
        #memberName5 = request.POST.get("memberName5", '')
        #memrelation5 = request.POST.get("memrelation5", '')
        #memBornDate5 = request.POST.get("memBornDate5", '')
        #EduLevel5 = request.POST.get("EduLevel5", '')
        #memPoliticalIdentity5 = request.POST.get('memPoliticalIdentity5', '')
        #memDepartmentPosition5 = request.POST.get('memDepartmentPosition5', '')
#
        #if (not (memberName5 == '' and memrelation5 == '')):
        #    familymember = FamilyMember()
        #    familymember.name = memberName5
        #    familymember.user = new_user
        #    familymember.relation = memrelation5
        #    familymember.BornDate = memBornDate5
        #    familymember.EducationLevel = EduLevel5
        #    familymember.PoliticalIdentity = memPoliticalIdentity5
        #    familymember.DepartmentPosition = memDepartmentPosition5
        #    familymember.save()
#
        #memberName6 = request.POST.get("memberName6", '')
        #memrelation6 = request.POST.get("memrelation6", '')
        #memBornDate6 = request.POST.get("memBornDate6", '')
        #EduLevel6 = request.POST.get("EduLevel6", '')
        #memPoliticalIdentity6 = request.POST.get('memPoliticalIdentity6', '')
        #memDepartmentPosition6 = request.POST.get('memDepartmentPosition6', '')
#
        #if (not (memberName6 == '' and memrelation6 == '')):
        #    familymember = FamilyMember()
        #    familymember.name = memberName6
        #    familymember.user = new_user
        #    familymember.relation = memrelation6
        #    familymember.BornDate = memBornDate6
        #    familymember.EducationLevel = EduLevel6
        #    familymember.PoliticalIdentity = memPoliticalIdentity6
        #    familymember.DepartmentPosition = memDepartmentPosition6
        #    familymember.save()

        # 民革关系
        for count in range(0, 6):
            relationid= request.POST.get("relationid"+str(count), '')
            relation1 = request.POST.get("relation"+str(count), '')
            relationName1 = request.POST.get("relationName"+str(count), '')
            BornDate1 = request.POST.get("BornDate"+str(count), '')
            BornDate1=ConfigInfo.getCorrectDate(BornDate1)
            EducationLevel1 = request.POST.get("EducationLevel"+str(count), '')
            PoliticalIdentity1 = request.POST.get("PoliticalIdentity"+str(count), '')
            DepartmentPosition1 = request.POST.get("DepartmentPosition"+str(count), '')
            IsLinkedNow1 = request.POST.get('IsLinkedNow'+str(count), '')

            if (not (relationName1 == '' and relation1 == '')):
                mingeRelation = None
                try:
                    mingeRelation = MinGeRelation.objects.get(id=int(relationid))
                except:
                    mingeRelation = MinGeRelation()

                mingeRelation.BornDate = BornDate1
                mingeRelation.relation = relation1
                mingeRelation.name = relationName1
                mingeRelation.user = new_user
                mingeRelation.EducationLevel = EducationLevel1
                mingeRelation.PoliticalIdentity = PoliticalIdentity1
                mingeRelation.DepartmentPosition = DepartmentPosition1
                mingeRelation.IsLinkedNow = IsLinkedNow1
                mingeRelation.save()

        #relation2 = request.POST.get("relation2", '')
        #relationName2 = request.POST.get("relationName2", '')
        #BornDate2 = request.POST.get("BornDate2", '')
        #EducationLevel2 = request.POST.get("EducationLevel2", '')
        #PoliticalIdentity2 = request.POST.get("PoliticalIdentity2", '')
        #DepartmentPosition2 = request.POST.get("DepartmentPosition2", '')
        #IsLinkedNow2 = request.POST.get('IsLinkedNow2', '')
#
        #if (not (relationName2 == '' and relation2 == '')):
        #    mingeRelation = MinGeRelation()
        #    mingeRelation.BornDate = BornDate2
        #    mingeRelation.relation = relation2
        #    mingeRelation.name = relationName2
        #    mingeRelation.user = new_user
        #    mingeRelation.EducationLevel = EducationLevel2
        #    mingeRelation.PoliticalIdentity = PoliticalIdentity2
        #    mingeRelation.DepartmentPosition = DepartmentPosition2
        #    mingeRelation.IsLinkedNow = IsLinkedNow2
        #    mingeRelation.save()
#
        #relation3 = request.POST.get("relation3", '')
        #relationName3 = request.POST.get("relationName3", '')
        #BornDate3 = request.POST.get("BornDate3", '')
        #EducationLevel3 = request.POST.get("EducationLevel3", '')
        #PoliticalIdentity3 = request.POST.get("PoliticalIdentity3", '')
        #DepartmentPosition3 = request.POST.get("DepartmentPosition3", '')
        #IsLinkedNow3 = request.POST.get('IsLinkedNow3', '')
#
        #if (not (relationName3 == '' and relation3 == '')):
        #    mingeRelation = MinGeRelation()
        #    mingeRelation.BornDate = BornDate3
        #    mingeRelation.relation = relation3
        #    mingeRelation.name = relationName3
        #    mingeRelation.user = new_user
        #    mingeRelation.EducationLevel = EducationLevel3
        #    mingeRelation.PoliticalIdentity = PoliticalIdentity3
        #    mingeRelation.DepartmentPosition = DepartmentPosition3
        #    mingeRelation.IsLinkedNow = IsLinkedNow3
        #    mingeRelation.save()
#
        #relation4 = request.POST.get("relation4", '')
        #relationName4 = request.POST.get("relationName4", '')
        #BornDate4 = request.POST.get("BornDate4", '')
        #EducationLevel4 = request.POST.get("EducationLevel4", '')
        #PoliticalIdentity4 = request.POST.get("PoliticalIdentity4", '')
        #DepartmentPosition4 = request.POST.get("DepartmentPosition4", '')
        #IsLinkedNow4 = request.POST.get('IsLinkedNow4', '')
#
        #if (not (relationName4 == '' and relation4 == '')):
        #    mingeRelation = MinGeRelation()
        #    mingeRelation.BornDate = BornDate4
        #    mingeRelation.relation = relation4
        #    mingeRelation.name = relationName4
        #    mingeRelation.user = new_user
        #    mingeRelation.EducationLevel = EducationLevel4
        #    mingeRelation.PoliticalIdentity = PoliticalIdentity4
        #    mingeRelation.DepartmentPosition = DepartmentPosition4
        #    mingeRelation.IsLinkedNow = IsLinkedNow4
        #    mingeRelation.save()
        #relation5 = request.POST.get("relation5", '')
        #relationName5 = request.POST.get("relationName5", '')
        #BornDate5 = request.POST.get("BornDate5", '')
        #EducationLevel5 = request.POST.get("EducationLevel5", '')
        #PoliticalIdentity5 = request.POST.get("PoliticalIdentity5", '')
        #DepartmentPosition5 = request.POST.get("DepartmentPosition5", '')
        #IsLinkedNow5 = request.POST.get('IsLinkedNow5', '')
#
        #if (not (relationName5 == '' and relation5 == '')):
        #    mingeRelation = MinGeRelation()
        #    mingeRelation.BornDate = BornDate5
        #    mingeRelation.relation = relation5
        #    mingeRelation.name = relationName5
        #    mingeRelation.user = new_user
        #    mingeRelation.EducationLevel = EducationLevel5
        #    mingeRelation.PoliticalIdentity = PoliticalIdentity5
        #    mingeRelation.DepartmentPosition = DepartmentPosition5
        #    mingeRelation.IsLinkedNow = IsLinkedNow5
        #    mingeRelation.save()


        return render(request, "userinformation.html", {
            "Msg": "请修改页面后保存",
            "userinfo": new_user
        })
