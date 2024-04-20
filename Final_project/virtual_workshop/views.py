from django.shortcuts import redirect
from .models import Tools, Service, Jobs, JobTool
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout


# Create your views here.

from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'dashboard.html')


def tools(request):
    tools_list = Tools.objects.all()
    return render(request, 'tools.html', {'tools': tools_list})

@login_required
def add_tools(request):
    """Supports adding new tools to the database via an HTML form."""
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
@login_required
def buy_new_tool(request, tool_id):
    """you can add new tool to database without form"""
    tool = Tools.objects.get(id=tool_id)
    tool.quantity += 1
    tool.save()
    messages.success(request, f"Kupiłeś {tool.name}.")
    return redirect('tools')
@login_required
@require_POST
def delete_tool(request, tool_id):
    """You can delete tool from list"""
    tool = Tools.objects.get(id=tool_id)
    if tool.quantity > 1:
        tool.quantity -= 1
        tool.save()
    else:
        tool.delete()
    return redirect('tools')

@login_required
def tools_status(request, tool_id):
    tool = Tools.objects.get(Tools, id=tool_id)
    tool.in_job = 'in_job' in request.POST
    tool.in_service = 'in_service' in request.POST
    tool.save()
    return redirect('tools')


def jobs(request):
    """you can see all job here"""
    if request.method == 'GET':
        job_list = Jobs.objects.all()
        tools = Tools.objects.all()
    return render(request, 'jobs.html', {'jobs': job_list, 'tools': tools })


@login_required
@require_POST
def delete_job(request, job_id):
    job = Jobs.objects.get(id=job_id)
    job.delete()
    return redirect('jobs')

@login_required
def add_job(request):
    """You can add new job here"""
    if request.method == 'GET':
        return render(request, 'add_job.html')
    else:
        job_name = request.POST.get('job_name')
        address = request.POST.get('address')
        new_job = Jobs(job_name=job_name, address=address)
        new_job.save()
        return redirect('jobs')



@login_required
def add_tool_to_job(request):
    """Here you add tools to orders"""
    if request.method == 'POST':
        job_id = request.POST.get('job')
        tool_id = request.POST.get('tool')
        job = Jobs.objects.get(id=job_id)
        tool = Tools.objects.get(id=tool_id)
        JobTool.objects.create(job=job, tool=tool)
        if tool.quantity > 0:
            tool.quantity -= 1
            tool.in_job = True
            tool.save()
        return redirect('jobs')
    else:
        jobs = Jobs.objects.all()
        tools = Tools.objects.filter(quantity__gt=0)
        return render(request, 'add_tool_to_job.html', {'jobs': jobs, 'tools': tools})
@login_required
@require_POST
def remove_tool_from_job(request, job_id, tool_id):
    job = Jobs.objects.get(id=job_id)
    tool_id = request.POST.get('tool')
    tool = Tools.objects.get(id=tool_id)
    job.tools.remove(tool)
    tool.quantity += 1
    tool.in_job = False
    tool.save()
    return redirect('jobs')

def service(request):
    """checks the tool is ready for receipt"""
    services = Service.objects.all()
    for service in services:
        if service.expected_pickup_date < timezone.now().date() and not service.repaired:
            service.repaired = True
            service.save()
    return render(request, 'service.html', {'services': services})


@login_required
def add_tool_to_service(request):
    """Send tool to service"""
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


def add_user(request):
    """Create new user"""
    if request.method == 'GET':
        return render(request, 'add_user.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Ten email jest już zajęty.')
            return render(request, 'add_user.html')
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        new_user.save()
        messages.success(request, 'Twoje konto zostało pomyślnie założone!')
        return redirect('dashboard')

def login(request):
    """user login to the application"""
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Cześć {user} udało Ci się zalogować.")
            return redirect('dashboard')
        else:
            messages.error(request, "Błędny email lub hasło.")
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return render(request, 'dashboard.html')



