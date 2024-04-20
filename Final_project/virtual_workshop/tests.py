from django.test import TestCase
from .models import Tools, Service, Jobs
from django.urls import reverse

# Create your tests here.

class ToolModelTest(TestCase):
    def add_tool(self):
        Tools.object.create(name="Wiertarka", model="DHR 243", quantity=2, accessories="Wiertła", in_job=False, in_service=False)

    def add_tool(self):
        drill = Tools.object.get(name='Wiertarka')
        self.assertEquals(drill.model, "Dhr 243")
        self.assertEquals(drill.quantity, 2)
        self.assertEquals(drill.accessories, "Wiertła")
        self.assertEquals(drill.in_job)
        self.assertEquals(drill.in_service)

    def test_default_values(self):
        grinder = Tools.objects.create(name="Szlifierka", model="Makita 9557HNG")
        self.assertEqual(grinder.quantity, 0)
        self.assertFalse(grinder.in_job)
        self.assertFalse(grinder.in_service)

#class ServiceModelTest(TestCase):


class ToolsViewTest(TestCase):
    def setUp(self):
        Tools.objects.create(name="Wiertarka", model="XYZ", quantity=1, accessories="Wiertła")
        Tools.objects.create(name="Wkrętakra", model="ZYX", quantity=2, accessories="Brak")

    def tools_template(self):
        response = self.client.get(reverse('tools'))
        tools_in_context = response.context['tools']
        self.assertEqual(len(tools_in_context), 2)
        self.assertEqual(tools_in_context[0].name, "Wiertarka")
        self.assertEqual(tools_in_context[1].name, "Młotek")

class Buy_tool(TestCase):
    def setUp(self):
        self.tool = Tools.objects.create(name="Wiertarka", model="XYZ", quantity=3)

    def test_buy_new_tool_quantity(self):
        current_quantity = self.tool.quantity
        updated_tool = Tools.objects.get(id=self.tool.id)
        self.assertEqual(updated_tool.quantity, current_quantity + 1)

class DeleteToolTests(TestCase):
    def setUp(self):
        self.tool = Tools.objects.create(name="Wiertarka", model="xyz", quantity=20)

    def test_delete_tool(self):
        response = self.client.post(reverse('delete_tool', args=[self.tool.id]))
        updated_tool = Tools.objects.get(id=self.tool.id)
        self.assertEqual(updated_tool.quantity, 1)
        self.assertRedirects(response, reverse('tools'))

class JobsViewTests(TestCase):
    def setUp(self):
        Jobs.objects.create(job_name="Zlecenie", address="Adres")

    def test_jobs_view(self):
        response = self.client.get(reverse('jobs'))
        self.assertTrue('jobs' in response.context)
        self.assertTemplateUsed(response, 'jobs.html')

class DeleteJobTests(TestCase):
    def setUp(self):
        self.job = Jobs.objects.create(job_name="Zlecenie 1", address="Adres")

    def test_delete_job(self):
        job_id = self.job.id
        response = self.client.post(reverse('delete_job', args=(job_id,)))
        self.assertRedirects(response, reverse('jobs'))

class RepairToolTests(TestCase):
    def setUp(self):
        self.tool = Tools.objects.create(name="Wiertarka", model="xyz")
        self.service = Service.objects.create(
            tool=self.tool,
            fault_description="nid dziala",
            expected_pickup_date="2023-01-01",
            repaired=False
        )

    def test_repair_tool(self):
        service_id = self.service.id
        response = self.client.post(reverse('repair_tool', args=(service_id,)), {'repaired': 'True'})
        self.assertRedirects(response, reverse('service'))

class TakeFromServiceTests(TestCase):
    def setUp(self):
        self.tool = Tools.objects.create(name="Wiertarka", model="xyz")
        self.service = Service.objects.create(
            tool=self.tool,
            fault_description="nid dziala",
            expected_pickup_date="2023-01-01",
            repaired=False
        )

    def test_take_from_service(self):
        service_id = self.service.id
        response = self.client.post(reverse('take_from_service', args=(service_id,)))
        self.assertRedirects(response, reverse('service'))











