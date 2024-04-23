import pytest
from django.urls import reverse
from django.test import Client
from virtual_workshop.models import Tools, Jobs, JobTool, Service
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

@pytest.fixture
def authenticated_user(client, django_user_model):
    user = django_user_model.objects.create_user(username='user', password='password1')
    client.login(username='user', password='password1')
    return user

@pytest.fixture
def tool(django_user_model):
    tool = Tools.objects.create(name="Wiertarka", model="Super2000", quantity=2)
    return tool

@pytest.fixture
def job(django_user_model):
    return Jobs.objects.create(job_name="Zlecenie")

@pytest.fixture
def service(django_user_model):
    return Service.objects.create(
        tool=tool,
        fault_description="proszę to naprawić",
        expected_pickup_date=timezone.now() - timezone.timedelta(days=1),
        repaired=True
    )



@pytest.mark.django_db
def test_dashboard_view(client):
    url = reverse('dashboard')
    response = client.get(url)
    assert response.status_code == 200
    assert 'dashboard.html' in (t.name for t in response.templates)

@pytest.mark.django_db
def test_tools_view_requires_login(client):
    url = reverse('tools')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_buy_tool(client, authenticated_user, tool):
    url = reverse('tools')
    response = client.post(url, {'action': 'buy', 'tool_id': tool.id})
    tool.refresh_from_db()
    assert tool.quantity == 3
    assert response.status_code == 302
    assert response.url == reverse('tools')
    messages = list(get_messages(response.wsgi_request))
    expected_message = f"Dodałeś '{tool.name} {tool.model}'."
    assert any(msg.message == expected_message for msg in messages)

@pytest.mark.django_db
def test_delete_tool_decreases_quantity(client, authenticated_user, tool):
    url = reverse('tools')
    response = client.post(url, {'action': 'delete', 'tool_id': tool.id})
    tool.refresh_from_db()
    assert tool.quantity == 1
    messages = list(get_messages(response.wsgi_request))
    expected_message = f"Ilość narzędzia {tool.name} {tool.model} została zmniejszona."
    assert any(msg.message == expected_message for msg in messages)

@pytest.mark.django_db
def test_update_status(client, django_user_model, tool):
    user = django_user_model.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    url = reverse('tools')
    response = client.post(url, {
        'action': 'update_status',
        'tool_id': tool.id,
        'in_job': 'on',
        'in_service': 'on'
    })
    tool.refresh_from_db()
    assert tool.in_job == True
    assert tool.in_service == True
    assert response.status_code == 302
    assert response.url == reverse('tools')
    response = client.post(url, {
        'action': 'update_status',
        'tool_id': tool.id,
    })
    tool.refresh_from_db()
    assert tool.in_job == False
    assert tool.in_service == False
    assert response.status_code == 302
    assert response.url == reverse('tools')




@pytest.mark.django_db
def test_jobs_view_requires_login(client):
    url = reverse('jobs')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_jobs_view(client, authenticated_user):
    url = reverse('jobs')
    response = client.get(url)
    assert response.status_code == 200
    assert 'jobs.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_add_job_view_get(client):
    url = reverse('add_job')
    response = client.get(url)
    assert response.status_code == 200
    assert 'add_job.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_add_job_post(client):
    url = reverse('add_job')
    data = {
        'job_name': 'Nazwa zlecenia',
        'address': 'Adres',
    }
    response = client.post(url, data)
    assert Jobs.objects.filter(job_name='Nazwa zlecenia').exists()
    assert response.status_code == 302
    assert response.url == reverse('jobs')

@pytest.mark.django_db
def test_get_add_tool_to_job(client):
    url = reverse('add_tool_to_job')
    response = client.get(url)
    assert response.status_code == 200
    assert 'add_tool_to_job.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_post_add_tool_to_job(client, authenticated_user, tool, job):
    url = reverse('add_tool_to_job')
    data = {
        'job': job.id,
        'tool': tool.id
    }
    response = client.post(url, data)
    tool.refresh_from_db()
    assert tool.quantity == 1
    assert tool.in_job is True
    assert JobTool.objects.filter(job=job, tool=tool).exists()
    assert response.status_code == 302
    assert response.url == reverse('jobs')

@pytest.mark.django_db
def test_service_view_tool_ready_to_take(client, authenticated_user, tool):
    service = Service.objects.create(
        tool=tool,
        fault_description="Nie dziala",
        expected_pickup_date=timezone.now() - timedelta(days=1),
        repaired=True
    )
    url = reverse('service')
    data = {'take_from_service': 'True', 'service_id': service.id}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('service')

@pytest.mark.django_db
def test_add_user_view_get(client):
    url = reverse('add_user')
    response = client.get(url)
    assert response.status_code == 200
    assert 'add_user.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_add_user_view_post_valid(client):
    url = reverse('add_user')
    data = {'username': 'user', 'email': 'user@example.com', 'password': 'password1'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('dashboard')
    assert User.objects.filter(username='user').exists()
    messages = list(get_messages(response.wsgi_request))
    assert any(message.message == 'Konto zostało utworzone!' for message in messages)

@pytest.mark.django_db
def test_login_view_get(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
    assert 'login.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_login_view_post_valid(client, authenticated_user):
    url = reverse('login')
    data = {'username': 'user', 'password': 'password1'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('dashboard')
    messages = list(get_messages(response.wsgi_request))
    assert any(f"Cześć {authenticated_user.username}, udało Ci się zalogować." in str(message) for message in messages)

def test_logout_view(client, authenticated_user):
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('dashboard')

















