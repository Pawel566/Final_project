from django.shortcuts import render, redirect
from django.views import View
from .models import Tools, Service
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponse

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

def tools_status(requset, tool_id):
    tool = Tools.objects.get(Tools, id=tool_id)
    tool.in_job = 'in_job' in request.POST
    tool.in_service = 'in_service' in request.POST
    tool.save()
    messages.success(request, "Status narzędzia został zaktualizowany.")
    return redirect('tools')


def jobs(request):
    return render(request, 'jobs.html')

def add_job(request):
    return render(request, 'add_job.html')

def add_tool_to_job(request):
    return render(request, 'add_tool_to_job.html')

def service(request):
    services = Service.objects.all()
    return render(request, 'service.html', {'services': services})


def add_tool_to_service(request):
    if request.method == 'GET':
        tools = Tools.objects.all()
        return render(request, 'add_tool_to_service.html', {'tools': tools})
    else:
        tool_id = request.POST.get('tool')
        tool = Tools.objects.get(id=tool_id)
        fault_description = request.POST.get('fault_description')
        expected_pickup_date = request.POST.get('expected_pickup_date')
        service = Service(tool=tool, fault_description=fault_description, expected_pickup_date=expected_pickup_date)
        service.save()
        return redirect('service')

@require_POST
def repair_tool(request, service_id):
    service = Service.objects.get(id=service_id)
    service.repaired = 'repaired' in request.POST
    service.save()
    return redirect('service')

@require_POST
def take_from_service(request, service_id):
    service = Service.objects.get(id=service_id)
    service.delete()
    return redirect('service')



