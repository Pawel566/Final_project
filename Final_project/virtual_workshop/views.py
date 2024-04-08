from django.shortcuts import render, redirect
from django.views import View
from .models import Tools
from django.contrib import messages
from django.views.decorators.http import require_POST

# Create your views here.

from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'dashboard.html')

def tools(requset):
    tools_list = Tools.objects.all()
    return render(requset, 'tools.html', {'tools': tools_list})

def add_tools(request):
    if request.method == 'GET':
        return render(request, 'add_tools.html')
    else:
        name = request.POST.get('name')
        model = request.POST.get('model')
        quantity = int(request.POST.get('quantity', 0))
        accessories = request.POST.get('accessories')
        tool = Tools(name=name, model=model, quantity=quantity, accessories=accessories)
        tool.save()
        messages.success(request, "Narzędzie zostało dodane!")
        return redirect('tools')

@require_POST
def delete_tool(request, tool_id):
    tool = Tools.objects.get(id=tool_id)
    tool.delete()
    return redirect('tools')


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

