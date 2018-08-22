# _*_ coding: utf-8 _*_
__author__ = 'Xialei'
__date__ = '2018/4/12 23:31'
# 用来form验证

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)

# class ModifypwdForm(forms.Form):
#     username = forms.CharField(required=True)
#     password1 = forms.CharField(required=True,min_length=5)
#     password2 = forms.CharField(required=True, min_length=5)

class AdduserForm(forms.Form):
    username = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    password1 = forms.CharField(required=True,min_length=5)
    password2 = forms.CharField(required=True, min_length=5)




class ModifypwdForm(forms.Form):
    password1= forms.CharField(required=True, min_length=5)
    password2= forms.CharField(required=True,min_length=5)

