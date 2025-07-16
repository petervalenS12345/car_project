from django.test import TestCase
from django.urls import reverse
from .models import Car
from .forms import CarForm
from django.contrib.messages import get_messages


class CarViewsTestCase(TestCase):
    def setUp(self):
        self.car1 = Car.objects.create(make='Car 1', color='Red', key=1.0)
        self.car2 = Car.objects.create(make='Car 2', color='Blue', key=2.0)
        self.car3 = Car.objects.create(make='Car 3', color='Red', key=3.0)

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual(len(response.context['cars']), 3)

    def test_dashboard_view_with_color_filter(self):
        response = self.client.get(reverse('dashboard'), {'color': 'Red'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual(len(response.context['cars']), 2)
        self.assertEqual(response.context['selected_color'], 'Red')

    def test_car_create_view_get(self):
        response = self.client.get(reverse('car_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cars/create.html')
        self.assertIsInstance(response.context['form'], CarForm)

    def test_car_create_view_post(self):
        data = {
            'make': 'New Car',
            'color': 'White',
        }
        response = self.client.post(reverse('car_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

        self.assertTrue(Car.objects.filter(make='New Car').exists())
        self.assertTrue(Car.objects.filter(color='White').exists())
        new_car = Car.objects.get(make='New Car')
        self.assertEqual(new_car.key, 4.0)

    def test_car_update_view_get(self):
        response = self.client.get(reverse('car_edit', kwargs={'pk': self.car1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cars/edit.html')
        self.assertIsInstance(response.context['form'], CarForm)

    def test_car_update_view_post(self):
        data = {
            'make': 'Updated Car',
            'color': 'Black',      # must be valid
            'position': 2          # position field required by view
        }
        response = self.client.post(reverse('car_edit', kwargs={'pk': self.car2.pk}), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('car_edit', kwargs={'pk': self.car2.pk}))

        updated_car = Car.objects.get(pk=self.car2.pk)
        self.assertEqual(updated_car.make, 'Updated Car')
        self.assertEqual(updated_car.color, 'Black')
        storage = get_messages(response.wsgi_request)
        messages = list(storage)

        self.assertTrue(any("Car updated successfully." in str(m) for m in messages))

    def test_car_delete_view(self):
        response = self.client.post(reverse('car_delete', kwargs={'id': self.car1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertFalse(Car.objects.filter(pk=self.car1.id).exists())
