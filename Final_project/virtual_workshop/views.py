from django.shortcuts import redirect
from .models import Tools, Service, Jobs, JobTool
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import (ToolForm, BuyNewToolForm, JobForm, AddToolToJobForm, AddToolToServiceForm,
                    TakeFromServiceForm, LoginForm, AddNewUser )
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

from django.shortcuts import render

class DashboardView(View):
    def get(self, request):
        return render(request, 'dashboard.html')


class ToolsView(LoginRequiredMixin, View):
    template_name = 'tools.html'
    login_url = reverse_lazy('login')

    def get(self, request, tool_id=None, action=None):
        if tool_id and action == 'buy':
            form = BuyNewToolForm(initial={'tool_id': tool_id})
            return render(request, self.template_name, {'form': form})
        tools_list = Tools.objects.all()
        return render(request, self.template_name, {'tools': tools_list})

    def post(self, request):
        action = request.POST.get('action')
        tool_id = request.POST.get('tool_id')
        if action == 'buy':
            return self.buy_tool(request, tool_id)
        elif action == 'delete':
            return self.delete_tool(request, tool_id)
        elif action == 'update_status':
            return self.update_status(request, tool_id)

        return redirect('tools')

    def buy_tool(self, request, tool_id):
        tool = Tools.objects.get(id=tool_id)
        tool.quantity += 1
        tool.save()
        messages.success(request, f"Dodałeś '{tool.name} {tool.model}'.")
        return redirect('tools')


    def delete_tool(self, request, tool_id):
        tool = Tools.objects.get(id=tool_id)
        if tool.quantity > 1:
            tool.quantity -= 1
            tool.save()
            messages.success(request, f"Ilość narzędzia {tool.name} {tool.model} została zmniejszona.")
        else:
            tool.delete()
            messages.success(request, f"Narzędzie {tool.name} {tool.model} zostało usunięte.")
        return redirect('tools')

    def update_status(self, request, tool_id):
        tool = Tools.objects.get(id=tool_id)
        tool.in_job = 'in_job' in request.POST
        tool.in_service = 'in_service' in request.POST
        tool.save()
        return redirect('tools')

class AddToolView(CreateView):
    model = Tools
    form_class = ToolForm
    template_name = 'add_tools.html'
    success_url = reverse_lazy('tools')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Narzędzie zostało dodane do warsztaty")
        return response




class JobsView(LoginRequiredMixin, View):
    template_name = 'jobs.html'
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        jobs = Jobs.objects.all()
        tools = Tools.objects.all()
        return render(request, self.template_name, {'jobs': jobs, 'tools': tools})

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == 'delete_job':
            return self.delete_job(request)
        elif action == 'remove_tool':
            return self.remove_tool(request)
        return redirect('jobs')

    def delete_job(self, request):
        job_id = request.POST.get('job_id')
        job = Jobs.objects.get(id=job_id)
        job.delete()
        return redirect('jobs')

    def remove_tool(self, request):
        job_id = request.POST.get('job_id')
        tool_id = request.POST.get('tool_id')
        job = Jobs.objects.get(id=job_id)
        tool = Tools.objects.get(id=tool_id)
        job.tools.remove(tool)
        tool.quantity += 1
        tool.in_job = False
        tool.save()
        messages.success(request, f"{tool.name} została usunięte ze zlecenia.")
        return redirect('jobs')


class AddJobView(CreateView):
    model = Jobs
    form_class = JobForm
    template_name = 'add_job.html'
    success_url = reverse_lazy('jobs')


class AddToolToJobView(View):
    template_name = 'add_tool_to_job.html'

    def get(self, request, *args, **kwargs):
        form = AddToolToJobForm()
        return render(request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):
        form = AddToolToJobForm(request.POST)

        if form.is_valid():
            job = form.cleaned_data['job']
            tool = form.cleaned_data['tool']

            if tool.quantity > 0:
                tool.quantity -= 1
                tool.in_job = True
                tool.save()
                JobTool.objects.create(job=job, tool=tool)
                messages.success(request, f"{tool.name} zostało dodane do zlecenia.")
                return redirect('jobs')
            else:
                messages.error(request, 'coś nie działaa.')

        return render(request, self.template_name, {'form': form})

class ServiceView(LoginRequiredMixin, View):
    template_name = 'service.html'
    login_url = reverse_lazy('login')


    def get(self, request, *args, **kwargs):
        services = Service.objects.all()
        for service in services:
            if service.expected_pickup_date < timezone.now().date() and not service.repaired:
                service.repaired = True
                service.save()
        return render(request, self.template_name, {'services': services})

    def post(self, request, *args, **kwargs):
        if 'take_from_service' in request.POST:
            form = TakeFromServiceForm(request.POST)
            if form.is_valid():
                service_id = form.cleaned_data['service_id']
                service = Service.objects.get(id=service_id)
                return self.take_from_service(request, service)
        elif 'repair_tool' in request.POST:
            service_id = request.POST.get('service_id')
            return self.repair_tool(request, service_id)

        return redirect('service')


    def take_from_service(self, request, service):
        tool = service.tool
        if tool.quantity >= 0:
            tool.quantity += 1
            tool.in_service = False
            tool.save()
            service.delete()
            messages.success(request, f"{tool.name} {tool.model} wróciła do warsztatu.")
        else:
            messages.error(request, 'Coś nie działa.')
        return redirect('service')

    def repair_tool(self, service_id):
        service = Service.objects.get(id=service_id)
        service.repaired = True
        service.save()
        return redirect('service')

class AddToolToServiceView(CreateView):
    model = Service
    form_class = AddToolToServiceForm
    template_name = 'add_tool_to_service.html'
    success_url = reverse_lazy('service')

    def form_valid(self, form):
        tool = form.cleaned_data['tool']
        if tool.quantity > 0:
            tool.quantity -= 1
            tool.in_service = True
            tool.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tools'] = Tools.objects.filter(quantity__gt=0)
        return context





class AddUserView(View):
    form_class = AddNewUser
    template_name = 'add_user.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Konto zostało utworzone!')
            return redirect('dashboard')
        else:
            return render(request, self.template_name, {'form': form})

class LoginView(View):
    form_class = LoginForm
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f"Cześć {user.username}, udało Ci się zalogować.")
            return redirect('dashboard')
        else:
            messages.error(request, "Błędny login lub hasło.")
            return render(request, self.template_name, {'form': form})

class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        return redirect('dashboard')

