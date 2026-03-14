from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Sum, Q, F
from django.utils import timezone
from django.urls import reverse_lazy
from .models import Product, Supplier, StockMovement
from .forms import ContactForm, SupplierForm, ProductForm, StockMovementForm
from accounts.decorators import manager_required
#     """
#     Displays a paginated list of products with search and filtering capabilities.
#     """
#     model = Product
#     template_name = 'core/device_list.html'
#     context_object_name = 'devices'
#     paginate_by = 10

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         form = DeviceSearchForm(self.request.GET)
#         if form.is_valid():
#             search = form.cleaned_data.get('search')
#             category = form.cleaned_data.get('category')

#             if search:
#                 queryset = queryset.filter(Q(name__icontains=search) | Q(code__icontains=search))
#             if category:
#                 queryset = queryset.filter(category=category)

#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = DeviceSearchForm(self.request.GET)
#         context['categories'] = Category.objects.all()
#         return context


# # Keep old name for compatibility with existing templates
# DeviceListView = ProductListView


# class ProductDetailView(LoginRequiredMixin, DetailView):
#     """
#     Displays detailed information about a specific product.
#     """
#     model = Product
#     template_name = 'core/device_detail.html'
#     context_object_name = 'device'


# # Keep old name for compatibility
# DeviceDetailView = ProductDetailView


class LandingPageView(TemplateView):
    """
    Landing page for the inventory management system.
    Shows different content for authenticated vs non-authenticated users.
    """
    template_name = 'core/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Show quick stats for authenticated users
            stats = {
                'total_products': Product.objects.filter(is_active=True).count(),
                'total_suppliers': Supplier.objects.count(),
                'low_stock_count': Product.objects.filter(quantity_in_stock__lte=F('reorder_level')).count(),
                'pending_invoices': Invoice.objects.filter(is_approved=False).count(),
            }
            context.update({
                'stats': stats,
                'total_products': stats['total_products'],
                'low_stock_products': stats['low_stock_count'],
                'total_suppliers': stats['total_suppliers'],
                'total_customers': Customer.objects.count(),
                'recent_movements': StockMovement.objects.select_related('product').order_by('-created_at')[:5],
            })
        return context


class ManagerDashboardView(LoginRequiredMixin, TemplateView):
    """
    Real-time manager monitoring dashboard showing all key metrics.
    """
    template_name = 'core/manager_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current date and today
        today = timezone.now().date()
        
        # Invoice metrics
        context['total_invoices'] = Invoice.objects.count()
        context['pending_invoices'] = Invoice.objects.filter(is_approved=False).count()
        context['overdue_invoices'] = Invoice.objects.filter(
            status='overdue',
            issue_date__lt=today
        ).count()
        context['total_invoice_value'] = Invoice.objects.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        # Receipt metrics
        context['total_receipts'] = Receipt.objects.count()
        context['pending_receipts'] = Receipt.objects.filter(is_approved=False).count()
        
        # Debt metrics
        context['total_outstanding_debt'] = Debt.objects.filter(
            status__in=['pending', 'partially_paid', 'overdue']
        ).aggregate(total=Sum('original_amount') - Sum('paid_amount'))['total'] or 0
        context['overdue_debts'] = Debt.objects.filter(
            status__in=['pending', 'partially_paid', 'overdue'],
            due_date__lt=today
        ).count()
        
        # Inventory metrics
        context['low_stock_products'] = Product.objects.filter(
            quantity_in_stock__lte=F('reorder_level')
        ).count()
        context['total_products'] = Product.objects.count()
        
        # Organization metrics
        context['total_customers'] = Customer.objects.count()
        context['total_suppliers'] = Supplier.objects.count()
        
        # Recent transactions
        context['recent_invoices'] = Invoice.objects.select_related('customer').order_by('-created_at')[:5]
        context['recent_receipts'] = Receipt.objects.select_related('supplier').order_by('-created_at')[:5]
        context['recent_debts'] = Debt.objects.select_related('customer').filter(
            status__in=['pending', 'partially_paid', 'overdue']
        ).order_by('-created_at')[:5]
        
        return context


class SupplierListView(LoginRequiredMixin, ListView):
    """
    Displays a paginated list of suppliers.
    """
    model = Supplier
    template_name = 'core/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 15
    ordering = ['name']


class SupplierDetailView(LoginRequiredMixin, DetailView):
    """
    Displays detailed information about a specific supplier.
    """
    model = Supplier
    template_name = 'core/supplier_detail.html'
    context_object_name = 'supplier'


class SupplierCreateView(LoginRequiredMixin, CreateView):
    """
    Creates a new supplier. Requires manager role.
    """
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
    """
    Updates an existing supplier. Requires manager role.
    """
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
    """
    Displays a paginated list of products with search and filtering capabilities.
    """
    model = Product
    template_name = 'core/product_list.html'
    context_object_name = 'products'
    paginate_by = 15

    def get_queryset(self):
        queryset = Product.objects.select_related('category', 'default_supplier')

        # Search by name
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(code__icontains=search)
            )

        # Filter by supplier
        supplier_id = self.request.GET.get('supplier_id')
        if supplier_id:
            queryset = queryset.filter(default_supplier_id=supplier_id)

        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suppliers'] = Supplier.objects.all()
        context['search'] = self.request.GET.get('search', '')
        context['supplier_id'] = self.request.GET.get('supplier_id', '')
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Displays detailed information about a specific product.
    """
    model = Product
    template_name = 'core/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.select_related('category', 'default_supplier')


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Creates a new product. Requires manager role.
    """
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
    """
    Updates an existing product. Requires manager role.
    """
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
    """
    Creates a new stock movement and updates product stock accordingly.
    Requires manager role.
    """
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
        # Check for stock out exceeding current stock
        if form.instance.movement_type == 'out':
            current_stock = form.instance.product.quantity_in_stock
            if form.instance.quantity > current_stock:
                form.add_error('quantity', f"Cannot remove {form.instance.quantity} items. Only {current_stock} items in stock.")
                return self.form_invalid(form)

        # Save the movement
        form.instance.created_by = self.request.user
        response = super().form_valid(form)

        # Update product stock
        product = form.instance.product
        if form.instance.movement_type == 'in':
            product.quantity_in_stock += form.instance.quantity
        elif form.instance.movement_type == 'out':
            product.quantity_in_stock -= form.instance.quantity
        product.save()

        messages.success(self.request, f"Stock movement recorded successfully. {form.instance.product.name} stock updated.")
        return response


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
