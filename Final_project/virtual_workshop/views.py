from django.shortcuts import render, redirect
from .models import Tools, Service, Jobs
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone

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

def buy_new_tool(request, tool_id):
    tool = Tools.objects.get(id=tool_id)
    tool.quantity += 1
    tool.save()
    messages.success(request, f"Ilość narzędzia {tool.name} została zwiększona.")
    return redirect('tools')
@require_POST
def delete_tool(request, tool_id):
    tool = Tools.objects.get(id=tool_id)
    if tool.quantity > 1:
        tool.quantity -= 1
        tool.save()
    else:
        tool.delete()
    return redirect('tools')

def tools_status(request, tool_id):
    tool = Tools.objects.get(Tools, id=tool_id)
    tool.in_job = 'in_job' in request.POST
    tool.in_service = 'in_service' in request.POST
    tool.save()
    return redirect('tools')


def jobs(request):
    job_list = Jobs.objects.all()
    return render(request, 'jobs.html', {'jobs': job_list})


@require_POST
def delete_job(request, job_id):
    job = Jobs.objects.get(id=job_id)
    job.delete()
    return redirect('jobs')

def add_job(request):
    if request.method == 'GET':
        return render(request, 'add_job.html')
    else:
        job_name = request.POST.get('job_name')
        address = request.POST.get('address')
        new_job = Jobs(job_name=job_name, address=address)
        new_job.save()
        return redirect('jobs')



def add_tool_to_job(request):
    if request.method == 'GET':
        jobs = Jobs.objects.all()
        tools = Tools.objects.filter(quantity__gt=0)
    return render(request, 'add_tool_to_job.html', {'jobs': jobs, 'tools': tools})

def service(request):
    services = Service.objects.all()
    for service in services:
        if service.expected_pickup_date < timezone.now().date() and not service.repaired:
            service.repaired = True
            service.save()
    return render(request, 'service.html', {'services': services})


def add_tool_to_service(request):
    if request.method == 'GET':
        tools = Tools.objects.filter(quantity__gt=0)
        return render(request, 'add_tool_to_service.html', {'tools': tools})
    else:
        tool_id = request.POST.get('tool')
        tool = Tools.objects.get(id=tool_id)
        if tool.quantity > 0:
            tool.quantity -= 1
            tool.in_service = True
            tool.save()
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
    tool = service.tool
    tool.quantity += 1
    tool.in_service = False
    tool.save()
    service.delete()
    return redirect('service')



