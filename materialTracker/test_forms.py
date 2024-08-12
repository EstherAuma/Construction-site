from django.test import TestCase
from materialTracker.forms import WorkerForm, MaterialForm
from materialTracker.models import Worker, Material

class TestWorkerForm(TestCase):
    def setUp(self):
        self.valid_data={
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '+256772014557',
            'email': 'deo@gmail.com'
        }

        self.invalid_data={
            'first_name': '',
            'last_name': '',
            'phone_number': '123456',
            'email':'deo'
        }

    def test_worker_form_valid(self):
        form = WorkerForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_worker_form_invalid(self):
        form = WorkerForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())

    def test_worker_form_save(self):
        form = WorkerForm(data=self.valid_data)
        form.is_valid()
        form.save()
        self.assertEqual(Worker.objects.count(), 1)

class TestMaterialForm(TestCase):
    def setUp(self):
        self.valid_data={
            'name': 'Cement',
            'unit': 'Bag'
        }

        self.invalid_data={
            'name': '',
            'unit': ''
        }

    def test_material_form_valid(self):
        form = MaterialForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_material_form_invalid(self):
        form = MaterialForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())

    def test_material_form_save(self):
        form = MaterialForm(data=self.valid_data)
        form.is_valid()
        form.save()
        self.assertEqual(Material.objects.count(), 1)
