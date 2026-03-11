from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Sum, Q, F
from django.utils import timezone
from .models import Product, Category, Invoice, Receipt, Debt, Customer, Supplier
from .forms import DeviceSearchForm, ContactForm


class ProductListView(LoginRequiredMixin, ListView):
    """
    Displays a paginated list of products with search and filtering capabilities.
    """
    model = Product
    template_name = 'core/device_list.html'
    context_object_name = 'devices'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        form = DeviceSearchForm(self.request.GET)
        if form.is_valid():
            search = form.cleaned_data.get('search')
            category = form.cleaned_data.get('category')

            if search:
                queryset = queryset.filter(Q(name__icontains=search) | Q(code__icontains=search))
            if category:
                queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DeviceSearchForm(self.request.GET)
        context['categories'] = Category.objects.all()
        return context


# Keep old name for compatibility with existing templates
DeviceListView = ProductListView


class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Displays detailed information about a specific product.
    """
    model = Product
    template_name = 'core/device_detail.html'
    context_object_name = 'device'


# Keep old name for compatibility
DeviceDetailView = ProductDetailView


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


def device_comparison_view(request, pk1=None, pk2=None):
    """
    Comparison view - keeping for compatibility but redirecting to dashboard.
    """
    messages.info(request, 'Device comparison feature has been replaced with inventory management tools.')
    return redirect('core:manager_dashboard')


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
