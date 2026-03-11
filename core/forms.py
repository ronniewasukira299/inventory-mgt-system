from django import forms
from .models import Product, Category, Invoice, Receipt, Debt, Customer, Supplier


class DeviceSearchForm(forms.Form):
    """Search form for products (keeping name for template compatibility)."""
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search products...'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label="All Categories")


class ProductSearchForm(forms.Form):
    """Search form for products."""
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search by name or code...'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label="All Categories")
    is_active = forms.BooleanField(required=False, label="Active products only")


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)


# ============================================================================
# INVOICING FORMS
# ============================================================================

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'customer', 'issue_date', 'due_date', 'notes']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


# ============================================================================
# RECEIPT FORMS
# ============================================================================

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['receipt_number', 'supplier', 'receipt_date', 'po_number', 'notes']
        widgets = {
            'receipt_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


# ============================================================================
# CUSTOMER & SUPPLIER FORMS
# ============================================================================

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'contact_person', 'email', 'phone', 'address', 'city', 'country', 'postal_code', 'credit_limit', 'credit_terms_days', 'status', 'notes']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'email', 'phone', 'address', 'city', 'country', 'postal_code', 'credit_terms_days', 'status', 'notes']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


# ============================================================================
# DEBT FORMS
# ============================================================================

class DebtPaymentForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = ['status']