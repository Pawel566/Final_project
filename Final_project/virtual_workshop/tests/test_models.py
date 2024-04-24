import pytest
from virtual_workshop.models import Tools, Jobs, Service
from django.utils import timezone

@pytest.fixture
def tool():
    tool = Tools.objects.create(
        name="Wiertarka",
        model="super2000",
        quantity=2,
        accessories="Wiertła",
        in_job=True,
        in_service=False
    )
    return tool

@pytest.fixture
def service(tool):
    return Service.objects.create(
        tool=tool,
        fault_description="Wydaje dziwne dzwięki",
        expected_pickup_date=timezone.now().date() + timezone.timedelta(days=3),
        repaired=False
    )

@pytest.fixture
def job(tool):
    job = Jobs.objects.create(
        job_name="Malowanie",
        address="Prosta 123"
    )
    return job

@pytest.mark.django_db
class TestToolsModel:
    def test_tool_fields(self, tool):
        assert tool.name == "Wiertarka"
        assert tool.model == "super2000"
        assert tool.quantity == 2
        assert tool.accessories == "Wiertła"
        assert tool.in_job is True
        assert tool.in_service is False

    def test_tool_field_lengths(self, tool):
        assert len(tool.name) <= 100
        assert len(tool.model) <= 100
        assert len(tool.accessories) <= 255

    def test_default_values(self, tool):
        assert tool.quantity == 2
        assert tool.in_job is True
        assert tool.in_service is False

@pytest.mark.django_db
class TestServiceModel:
    def test_service(self, service):
        assert isinstance(service, Service)
        assert service.tool.name == "Wiertarka"
        assert service.fault_description == "Wydaje dziwne dzwięki"
        assert service.repaired is False

    def test_expected_pickup_date(self, service):
        assert service.expected_pickup_date > timezone.now().date()

@pytest.mark.django_db
class TestJobsModel:
    def test_job_add(self, job):
        assert job.job_name == "Malowanie"
        assert job.address == "Prosta 123"