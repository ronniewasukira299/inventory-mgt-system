from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Device, DeviceComparison, Category
from .forms import DeviceSearchForm, ContactForm

class DeviceListView(LoginRequiredMixin, ListView):
    """
    Displays a paginated list of devices with search and filtering capabilities.
    """
    model = Device
    template_name = 'core/device_list.html'
    context_object_name = 'devices'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        form = DeviceSearchForm(self.request.GET)
        if form.is_valid():
            search = form.cleaned_data.get('search')
            category = form.cleaned_data.get('category')
            device_type = form.cleaned_data.get('device_type')

            if search:
                queryset = queryset.filter(name__icontains=search)
            if category:
                queryset = queryset.filter(category=category)
            if device_type:
                queryset = queryset.filter(type=device_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DeviceSearchForm(self.request.GET)
        context['categories'] = Category.objects.all()
        return context

class DeviceDetailView(LoginRequiredMixin, DetailView):
    """
    Displays detailed information about a specific device.
    """
    model = Device
    template_name = 'core/device_detail.html'
    context_object_name = 'device'

def device_comparison_view(request, pk1, pk2):
    """
    Displays a comparison between two devices.
    """
    device1 = get_object_or_404(Device, pk=pk1)
    device2 = get_object_or_404(Device, pk=pk2)

    comparison, created = DeviceComparison.objects.get_or_create(
        device1=device1,
        device2=device2,
        defaults={'created_by': request.user, 'comparison_data': {}}
    )

    context = {
        'device1': device1,
        'device2': device2,
        'comparison': comparison,
    }
    return render(request, 'core/device_comparison.html', context)

def contact_view(request):
    """
    Handles contact form submissions.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form (e.g., send email)
            messages.success(request, 'Thank you for your message!')
            return redirect('core:contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})
