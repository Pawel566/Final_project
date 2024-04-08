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
from django.contrib import admin
from django.urls import path
from .views import (dashboard_view, tools, add_tools, jobs,
                                    service, add_job, add_tool_to_job, add_tool_to_service, delete_tool,
                    tools_status)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_view, name='dashboard'),
    path('tools/', tools, name='tools'),
    path('tools/add_tools_to_list/', add_tools, name='add_tools'),
    path('jobs/', jobs, name="jobs"),
    path('service/', service, name='service'),
    path('jobs/add_job/', add_job, name='add_job'),
    path('jobs/add_tool_to_job/', add_tool_to_job, name='add_tool_to_job'),
    path('service/add_tool_to_service/', add_tool_to_service, name='add_tool_to_service'),
    path('delete_tool/<int:tool_id>/', delete_tool, name='delete_tool'),
    path('tools/update_status/<int:tool_id>/', tools_status, name='update_tool_status'),
]
