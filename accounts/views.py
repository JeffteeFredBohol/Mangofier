from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Sale
from django.shortcuts import get_object_or_404
from difflib import SequenceMatcher
from django.db.models import Sum

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard')  # Create a dashboard view later
        else:
            messages.error(request, "Invalid credentials or not staff.")
    return render(request, 'accounts/login.html')

def home_redirect(request):
    return redirect('login')  # 'login' is the name we gave in the URL pattern

@login_required()
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect('login')

@login_required
def stock_view(request):
    products = Product.objects.all()
    return render(request, 'accounts/stock.html', {'products': products})

@login_required
def add_product(request):
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        quantity = request.POST['quantity']
        threshold = request.POST['threshold']

        for existing in Product.objects.all():
            similarity = SequenceMatcher(None, name.lower(), existing.name.lower()).ratio()
            if similarity > 0.8:
                messages.error(request, "Item name is too similar to an existing one.")
                return redirect('add_product')

        Product.objects.create(
            name=name,
            price=price,
            quantity=quantity,
            threshold=threshold
        )
        messages.success(request, "Item added successfully.")
        return redirect('stock')

    return render(request, 'accounts/add_product.html')


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.quantity = request.POST['quantity']
        product.threshold = request.POST['threshold']
        product.save()
        messages.success(request, "Item updated.")
        return redirect('stock')

    return render(request, 'accounts/edit_product.html', {'product': product})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Item deleted.")
        return redirect('stock')

    return render(request, 'accounts/confirm_delete.html', {'product': product})

@login_required
def record_sale(request):
    products = Product.objects.all()

    if request.method == 'POST':
        product_id = request.POST['product']
        quantity = int(request.POST['quantity'])

        product = get_object_or_404(Product, pk=product_id)

        if quantity > product.quantity:
            messages.error(request, "Not enough stock available.")
            return redirect('record_sale')

        # Record sale
        Sale.objects.create(product=product, quantity=quantity)

        # Update inventory
        product.quantity -= quantity
        product.save()

        messages.success(request, "Sale recorded successfully.")
        return redirect('record_sale')

    return render(request, 'accounts/record_sale.html', {'products': products})

@login_required
def profit_report(request):
    products = Product.objects.all()
    report_data = []
    total_sales = 0  # NEW

    for product in products:
        sales = Sale.objects.filter(product=product)
        total_sold = sales.aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_sales += total_sold  # Count total sales

        revenue = total_sold * product.price
        profit = revenue

        report_data.append({
            'product': product,
            'total_sold': total_sold,
            'revenue': revenue,
            'profit': profit
        })

    return render(request, 'accounts/profit_report.html', {
        'report_data': report_data,
        'total_sales': total_sales  # Send to template
    })

@login_required
def delete_all_sales(request):
    if request.method == "POST":
        Sale.objects.all().delete()
        messages.success(request, "All sales records have been deleted.")
        return redirect('profit_report')

    total_sales = Sale.objects.count()
    return render(request, 'accounts/confirm_delete_all_sales.html', {'total_sales': total_sales})