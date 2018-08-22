"""MinGe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, url
    2. Add a URL to urlpatterns:  url('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url,include
from django.views.generic import TemplateView
from Users import views
from django.views.static import serve  # 导入相关静态文件处理的views控制包
from .settings import MEDIA_ROOT  # 导入项目文件夹中setting中的MEDIA_ROOT绝对路


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$',  serve, {"document_root": MEDIA_ROOT}),

    url('^$', TemplateView.as_view(template_name="login.html")),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^index/$',views.index,name="index"),
    url(r'^deleteuser/$',views.DeleteInfo.as_view(),name="deleteinfo"),

    url(r'^activity/$',views.activityView,name="activity"),
    url(r'^leader/$',views.leader,name="leader"),
    url(r'^addresslist/$',views.addresslist.as_view(),name="addresslist"),

    url(r'^userlist/$',views.userlist.as_view(),name="userlist"),
    url(r'^userinformation/$',views.userinformation,name="userinformation"),
    url(r'^userinformation_add/$',views.userinformation_add.as_view(),name="userinformation_add"),
    # url(r'^userinformation_modify/$',views.userinformation_modify,name="userinformation_modify"),

    url(r'^modifyinfo/$', views.ModifyInfo.as_view(), name="modifyinfo"),
    url(r'^add_user/$',views.AdduserView.as_view(),name="add_user"),
    url(r'^delete_user/$',views.delete_user.as_view(),name="delete_user"),
    url(r'^user_manage/$',views.user_manage,name="user_manage"),
    url(r'^modify_user/$', views.ModifyUser.as_view(), name="modify_user"),
    url(r'^modify_pwd/$',views.ModifypwdView.as_view(),name="modify_pwd"),

    url(r'^search_name/$',views.search_name,name="search_name"),
    url(r'^search_address/$',views.search_address,name="search_address"),
    url(r'^search_userlist/$',views.search_userlist,name="search_userlist"),


]
