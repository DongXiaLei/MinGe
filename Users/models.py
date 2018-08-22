from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class ContactList(models.Model):
    name=models.CharField(max_length=200, verbose_name=u"姓名")
    MobilePhone=models.CharField(max_length=20, verbose_name=u"手机")
    qqNum=models.CharField(max_length=20, verbose_name=u"QQ号")
    gender=models.CharField(max_length=255,verbose_name=u"性别")
    BornDate=models.DateField(verbose_name=u"出生日期")
    nation=models.CharField(max_length=255, verbose_name=u"民族")
    EduExperience=models.CharField(max_length=100, verbose_name=u"教育经历")
    PropertyOfWorkUnit=models.CharField(max_length=100, verbose_name=u"教育经历")
    WorkUnit=models.CharField(max_length=100, verbose_name=u"工作职务")
    DateComeIntoMinGe=models.DateField(verbose_name=u"加入日期")
    BranchPartyName=models.CharField(max_length=255, verbose_name=u"支部名称")

    class  Meta:
        # db_table='ContactList'
        verbose_name=u"联系人"

class User(AbstractUser):
    phone = models.CharField(max_length=11,null=True)
    image = models.ImageField(upload_to="image/%Y/%m", default="", max_length=100)
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default="")
    is_manager = models.BooleanField(default=False)
    login_time = models.DateTimeField(default=timezone.now, verbose_name="登录时间")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

class baseInfo(models.Model):
    name = models.CharField(max_length=40,null=False)
    nameUsed = models.CharField(max_length=40,null=True,blank=True)
    nation = models.CharField(max_length=40,null=True,blank=True)
    NativePlace = models.CharField(max_length=100,null=True,blank=True)

    religious = models.CharField(max_length=40,null=True,blank=True)
    BornPlace = models.CharField(max_length=100,null=True,blank=True)
    BornDate = models.DateField()
    IDCardNum = models.CharField(max_length=40,null=False)
    PartyDocuNum = models.CharField(max_length=100,null=True,blank=True)

    BranchParty = models.CharField(max_length=100,null=True,blank=True)
    BranchPartyNum = models.CharField(max_length=100,null=True,blank=True)
    MobilePhone = models.CharField(max_length=20)
    email = models.EmailField(max_length=40,null=True,blank=True)
    img = models.ImageField(max_length=0,null=True,blank=True)

    def __str__(self):
        return self.name

class education(models.Model):
    college = models.CharField(max_length=100)
    user = models.ForeignKey(baseInfo,on_delete=models.CASCADE,null=False)
    major = models.CharField(max_length=100)
    ComeIntoSchoolDate = models.DateField()
    GraduateDate = models.DateField()
    EduDegree = models.CharField(max_length=100)
    EduExperience = models.CharField(max_length=100)
    EduType = models.CharField(max_length=100)

    def __str__(self):
        return self.college

class Work(models.Model):
    user = models.ForeignKey('baseInfo', on_delete=models.CASCADE, null=False)
    WorkUnit = models.CharField(max_length=100)
    WorkPosition = models.CharField(max_length=100,default='')
    PropertyOfWorkUnit = models.CharField(max_length=100)

    AdministrativeLevel = models.CharField(max_length=100,blank=True)
    WorkUnitAddr =models.CharField(max_length=255)
    WorkPhone = models.CharField(max_length=20)
    WorkPostcode =models.CharField(max_length=6)
    HomeAddr = models.CharField(max_length=255)

    HomePhone = models.CharField(max_length=20)
    HomePostcode = models.CharField(max_length=6)
    ContactAddrType = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    WelfareLevel = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Resume(models.Model):
    user = models.ForeignKey('baseInfo', on_delete=models.CASCADE, null=False)
    StartDate = models.DateField()
    EndDate = models.DateField()
    department = models.CharField(max_length=255)
    position = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class AwardInfo(models.Model):
    user = models.ForeignKey('baseInfo', on_delete=models.CASCADE, null=False)
    AwardDate = models.DateField()
    AwardLevel = models.CharField(max_length=255)
    HoldWorkUnit = models.CharField(max_length=255)
    AwardDetail = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Punish(models.Model):
    user = models.ForeignKey('baseInfo', on_delete=models.CASCADE, null=False)
    PunishDate = models.DateField()
    details = models.CharField(max_length=255)
    CancelDetail = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class PositionSincePast(models.Model):
    user = models.ForeignKey('baseInfo', on_delete=models.CASCADE, null=False)
    StartDate = models.DateField()
    EndDate = models.DateField()
    department = models.CharField(max_length=255)
    position = models.CharField(max_length=255,null=True,blank=True)
    WorkType = models.CharField(max_length=255)
    Which = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class activity(models.Model):
    user = models.ForeignKey('baseInfo', on_delete=models.CASCADE, null=False)
    StartDate = models.DateField()
    ActivityName = models.CharField(max_length=255)
    addr = models.CharField(max_length=255)
    introducer = models.CharField(max_length=255)
    PositionOfIntroducer = models.CharField(max_length=255)
    IsLinkedNow = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class MinGeRelation(models.Model):
    user = models.ForeignKey('baseInfo', on_delete=models.CASCADE, null=False)
    BornDate = models.DateField()
    name = models.CharField(max_length=255)
    relation = models.CharField(max_length=255)
    EducationLevel = models.CharField(max_length=255)
    PoliticalIdentity = models.CharField(max_length=255)
    DepartmentPosition = models.CharField(max_length=255)
    IsLinkedNow = models.CharField(max_length=255)


    def __str__(self):
        return self.name

class FamilyMember(models.Model):
    user = models.ForeignKey('baseInfo', on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=255)
    relation = models.CharField(max_length=255)
    BornDate = models.DateField()
    EducationLevel = models.CharField(max_length=255)
    PoliticalIdentity = models.CharField(max_length=255)
    DepartmentPosition = models.CharField(max_length=255)

    def __str__(self):
        return self.name
