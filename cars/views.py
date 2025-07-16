# Create your views here.
from django.shortcuts import redirect, get_object_or_404
from .forms import CarForm
from django.db.models import Max
from django.db import transaction
from django.db.models import F
from .models import Car
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib import messages




def dashboard(request):
    color_filter = request.GET.get('color')

    if color_filter:
        cars = Car.objects.filter(color=color_filter).order_by('key')
    else:
        cars = Car.objects.all().order_by('key')

    colors = sorted(set(Car.objects.values_list('color', flat=True)))

    return render(request, 'dashboard.html', {
        'cars': cars,
        'colors': colors,
        'selected_color': color_filter
    })


def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            last_key = Car.objects.aggregate(Max('key'))['key__max'] or 0.0
            new_car = form.save(commit=False)
            new_car.key = last_key + 1.0  # ✅ Assign new key
            new_car.save()
            return redirect('dashboard')  # You can change this to 'dashboard' if preferred
    else:
        form = CarForm()
    return render(request, 'cars/create.html', {'form': form})



class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'cars/edit.html'

    def get_success_url(self):
        return reverse_lazy('car_edit', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)

        try:
            position = int(self.request.POST.get('position'))  # Match form field name
        except (TypeError, ValueError):
            messages.error(self.request, "Invalid position.")
            return response

        car = self.object
        total_cars = Car.objects.count()

        # Validate position range
        target_car = (
            Car.objects.order_by('key')[position - 1]
            if 0 < position <= total_cars
            else None
        )

        before = Car.objects.filter(key__lt=target_car.key).order_by('-key').first() if target_car else None
        after = target_car

        if before and after:
            car.key = (before.key + after.key) / 2
        elif after:
            car.key = after.key - 1
        elif before:
            car.key = before.key + 1
        else:
            car.key = 1

        car.save(update_fields=['key'])
        messages.success(self.request, "Car updated successfully.")
        return response
def car_delete(request, id):
    car = get_object_or_404(Car, pk=id)
    car.delete()
    return redirect('dashboard')