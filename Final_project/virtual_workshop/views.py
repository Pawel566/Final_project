from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'index.html')

def tools(requset):
    return render(requset, 'tools.html')

def add_tools_to_list(request):
    return render(request, 'add_tools_to_list.html')

def jobs(request):
    return render(request, 'jobs.html')

def add_job(request):
    return render(request, 'add_job.html')

def add_tool_to_job(request):
    return render(request, 'add_tool_to_job.html')

def service(request):
    return render(request, 'service.html')

def add_tool_to_service(request):
    return render(request, 'add_tool_to_service.html')

