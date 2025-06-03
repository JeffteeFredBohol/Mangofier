from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Stock, Sale
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ConfirmSaleForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


# Create your views here.
@method_decorator(never_cache, name='dispatch')
class StockListView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = 'stock_list.html'
    context_object_name = 'stocks'
    login_url = '/accounts/login/'

@method_decorator(never_cache, name='dispatch')
class StockCreateView(LoginRequiredMixin, CreateView):
    model = Stock
    fields = ['name', 'quantity', 'price', 'reorder_level']  # ✅ added reorder_level
    template_name = 'stock_form.html'
    success_url = reverse_lazy('stock_list')
    login_url = '/accounts/login/'

@method_decorator(never_cache, name='dispatch')
class StockUpdateView(LoginRequiredMixin, UpdateView):
    model = Stock
    fields = ['name', 'quantity', 'price', 'reorder_level']  # ✅ added reorder_level
    template_name = 'stock_form.html'
    success_url = reverse_lazy('stock_list')
    login_url = '/accounts/login/'

@method_decorator(never_cache, name='dispatch')
class StockDeleteView(LoginRequiredMixin, DeleteView):
    model = Stock
    template_name = 'stock_confirm_delete.html'
    success_url = '/'
    login_url = '/accounts/login/'

@method_decorator(never_cache, name='dispatch')
class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sale_list.html'
    context_object_name = 'sales'

@method_decorator(never_cache, name='dispatch')
class SaleCreateView(LoginRequiredMixin, CreateView):
    model = Sale
    fields = ['stock', 'quantity_sold', 'sale_price']
    template_name = 'sale_form.html'
    success_url = '/sales/'

@method_decorator(never_cache, name='dispatch')
class SalesSummaryView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales_summary.html'
    context_object_name = 'sales'

    def get_queryset(self):
        return Sale.objects.select_related('stock')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sales = self.get_queryset()
        total_sales = sum([sale.sale_price * sale.quantity_sold for sale in sales])
        context['total_sales'] = total_sales
        return context

@never_cache
@login_required
def confirm_sale_view(request):
    if request.method == 'POST':
        form = ConfirmSaleForm(request.POST)
        if form.is_valid():
            stock_id = form.cleaned_data['stock_id']
            quantity = form.cleaned_data['quantity_sold']

            stock = get_object_or_404(Stock, id=stock_id)

            if stock.quantity < quantity:
                messages.error(request, 'Not enough stock to complete the sale.')
            else:
                Sale.objects.create(
                    stock=stock,
                    quantity_sold=quantity,
                    sale_price=stock.price  # ✅ Auto-uses the stock's price
                )
                stock.quantity -= quantity
                stock.save()
                messages.success(request, f"Sale recorded: {quantity} x {stock.name} at ₱{stock.price}")
                return redirect('sale_confirm')
    else:
        form = ConfirmSaleForm()

    return render(request, 'confirm_sale.html', {'form': form})

def home_redirect_view(request):
    if request.user.is_authenticated:
        return redirect('stock_list')  # or any other default page
    else:
        return redirect('login')
