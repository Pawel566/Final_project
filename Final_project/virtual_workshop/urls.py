"""
URL configuration for Final_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib.auth import logout
from django.contrib import admin
from django.urls import path
from .views import (DashboardView, ToolsView, AddToolView, JobsView, ServiceView, AddJobView, AddToolToJobView,
                    AddToolToServiceView, AddUserView, LoginView, LogoutView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DashboardView.as_view(), name='dashboard'),
    path('tools/', ToolsView.as_view(), name='tools'),
    path('tools/add_tools_to_list/', AddToolView.as_view(), name='add_tools'),
    path('jobs/', JobsView.as_view(), name="jobs"),
    path('service/', ServiceView.as_view(), name='service'),
    path('add_job/', AddJobView.as_view(), name='add_job'),
    path('jobs/add_tool_to_job/', AddToolToJobView.as_view(), name='add_tool_to_job'),
    path('service/add_tool_to_service/', AddToolToServiceView.as_view(), name='add_tool_to_service'),
    path('add_user/', AddUserView.as_view(), name='add_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
