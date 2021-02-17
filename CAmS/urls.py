"""CAmS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from FrontSite import views as main_site
from MainPage.views import StartPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<int:id>/', main_site.FrontPage, name="FrontPage"),
    path('', main_site.StartPage, name="StartPage"),
    re_path(r"logout(\?next=(?P<next>\w+))?$", main_site.Logout, name="logout"),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('UserControl.urls')),  # Actions with users
    path('project/', include('ProjectControl.urls')),  # Actions with projects
    path('', StartPage, name="start_page"),
    re_path('^action=(?P<action>\w+)$',
            StartPage,
            name="start_page_with_action"),
]


