from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.urls import reverse_lazy
from .models import Product, Supplier, StockMovement
from .forms import ContactForm, SupplierForm, ProductForm, StockMovementForm


class LandingPageView(TemplateView):
    template_name = 'core/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context.update({
                'total_products': Product.objects.filter(is_active=True).count(),
                'total_suppliers': Supplier.objects.count(),
                'low_stock_products': Product.objects.filter(stock_quantity__lte=10).count(),
                'recent_movements': StockMovement.objects.select_related('product').order_by('-created_at')[:5],
            })
        return context


class ManagerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/manager_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_products'] = Product.objects.count()
        context['total_suppliers'] = Supplier.objects.count()
        context['low_stock_products'] = Product.objects.filter(stock_quantity__lte=10).count()
        context['recent_movements'] = StockMovement.objects.select_related('product').order_by('-created_at')[:5]
        return context


class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'core/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 15
    ordering = ['name']


class SupplierDetailView(LoginRequiredMixin, DetailView):
    model = Supplier
    template_name = 'core/supplier_detail.html'
    context_object_name = 'supplier'


class SupplierCreateView(LoginRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'core/supplier_form.html'
    success_url = reverse_lazy('core:supplier_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'manager':
            messages.error(request, "Access denied. Manager role required.")
            return redirect('core:supplier_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f"Supplier '{form.instance.name}' created successfully.")
        return super().form_valid(form)


class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'core/supplier_form.html'
    success_url = reverse_lazy('core:supplier_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'manager':
            messages.error(request, "Access denied. Manager role required.")
            return redirect('core:supplier_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, f"Supplier '{form.instance.name}' updated successfully.")
        return super().form_valid(form)


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'core/product_list.html'
    context_object_name = 'products'
    paginate_by = 15

    def get_queryset(self):
        queryset = Product.objects.select_related('supplier')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(name__icontains=search))
        supplier_id = self.request.GET.get('supplier_id')
        if supplier_id:
            queryset = queryset.filter(supplier_id=supplier_id)
        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suppliers'] = Supplier.objects.all()
        context['search'] = self.request.GET.get('search', '')
        context['supplier_id'] = self.request.GET.get('supplier_id', '')
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'core/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.select_related('supplier')


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'core/product_form.html'
    success_url = reverse_lazy('core:product_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'manager':
            messages.error(request, "Access denied. Manager role required.")
            return redirect('core:product_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f"Product '{form.instance.name}' created successfully.")
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'core/product_form.html'
    success_url = reverse_lazy('core:product_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'manager':
            messages.error(request, "Access denied. Manager role required.")
            return redirect('core:product_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, f"Product '{form.instance.name}' updated successfully.")
        return super().form_valid(form)


class StockMovementCreateView(LoginRequiredMixin, CreateView):
    model = StockMovement
    form_class = StockMovementForm
    template_name = 'core/stock_movement_form.html'
    success_url = reverse_lazy('core:product_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'manager':
            messages.error(request, "Access denied. Manager role required.")
            return redirect('core:product_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.instance.movement_type == 'out':
            current_stock = form.instance.product.stock_quantity
            if form.instance.quantity > current_stock:
                form.add_error('quantity', f"Cannot remove {form.instance.quantity} items. Only {current_stock} in stock.")
                return self.form_invalid(form)
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        product = form.instance.product
        if form.instance.movement_type == 'in':
            product.stock_quantity += form.instance.quantity
        elif form.instance.movement_type == 'out':
            product.stock_quantity -= form.instance.quantity
        product.save()
        messages.success(self.request, f"Stock movement recorded. {product.name} stock updated.")
        return response


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Thank you for your message!')
            return redirect('core:contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})