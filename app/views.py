from unicodedata import name
from django.shortcuts import render, redirect, get_object_or_404



# Database 
from .models import *
# Forms
from .forms import *
# InitialFactory form
from django.forms import inlineformset_factory

# Authentication views
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# decorators.py
from .decorators import unauthenticated_user, allowed_users, admin_only

# Grouping views
from django.contrib.auth.models import Group


@unauthenticated_user
def register(request):
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            # Signals part --> make auto profile for user if he is normal user
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                name=request.POST['name'],
                email=request.POST['email'],
                phone=request.POST['phone'],
                address=request.POST['address'],
            )
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {
        'form': form
    }
    return render(request, 'registeration/register.html', context)



@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'registeration/login.html', context)



@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')


# @login_required(login_url='login')
@admin_only
def home(request):

    # Retrieve all orders
    orders = Order.objects.all()
    total_orders = orders.count()

    # Retrieve all customers
    customers = Customer.objects.all()
    total_customers = customers.count()

    # Retrieve all products
    products = Product.objects.all()
    total_products = products.count()

    # Retrieve all delivered orders
    delivered = Order.objects.filter(status='Delivered')  # Filter orders by status
    delivered_count = delivered.count()

    # Retrieve all pending orders
    pending = Order.objects.filter(status='Pending')
    pending_count = pending.count()


    context = {
        'orders': orders,
        'total_orders': total_orders,
        'customers': customers,
        'total_customers': total_customers,
        'products': products,
        'total_products': total_products,
        'delivered': delivered,
        'pending': pending,
        'delivered_count': delivered_count,
        'pending_count': pending_count,
    }

    return render(request, 'pages/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    user_orders = request.user.customer.order_set.all()  # Get all orders for the logged in customer
    user_total_orders = user_orders.count()
    user_delivered = user_orders.filter(status='Delivered').count()
    user_pending = user_orders.filter(status='Pending').count()


    context = {
        'user_orders': user_orders,
        'user_total_orders': user_total_orders,
        'user_delivered': user_delivered,
        'user_pending': user_pending,
    }
    return render(request, 'pages/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'pages/account_settings.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):

    all_products = Product.objects.all()
    return render(request, 'pages/products.html', {'all_products': all_products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def add_product(request):
    form = ProductForm()
    image = request.FILES.get('image')
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')

    context = {
        'form': form,
        'image': image,
    }
    return render(request, 'pages/add_product.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'pages/product.html', {'product': product})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_product(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    image = product.image
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')

    context = {
        'form': form,
        'image': image,
    }
    return render(request, 'pages/update_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products')

    context = {
        'product': product,
    }
    return render(request, 'pages/delete_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def search_view(request):
    if request.method == 'POST':
        searched = request.POST['query'] # Get the searched value
        products = Product.objects.filter(name__contains=searched)
        counting = products.count()
        return render(request, 'parts/search.html', {'searched': searched, 'products': products, 'counting': counting})
    else:
        return render(request, 'parts/search.html', {})


@login_required(login_url='login')
@allowed_users(['admin'])
def customers(request):

    customers = Customer.objects.all()
    context = {
        'customers': customers
    }
    return render(request, 'pages/customers.html', context)


# Q objects are used to combine multiple filters
from django.db.models import Q

@login_required(login_url='login')
@allowed_users(['admin'])
def search_customer(request):
    if request.method == 'POST':
        searched = request.POST.get('search', None) 
        
        if searched:
            customers = Customer.objects.filter(Q(name__icontains=searched) | Q(id__icontains=searched))
            counting = customers.count()
            return render(request, 'pages/search_customer.html', {'customers': customers, 'counting': counting})
        else:
            return render(request, 'pages/search_customer.html', {})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    
    # Retrieve customer by id
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        return redirect('home')

    orders = customer.order_set.all()
    order_count = orders.count()

    # filters
    from .filters import OrderFilter
    
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs 

    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'myFilter': myFilter,
    }

    return render(request, 'pages/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('home')

    context = {
        'customer': customer
    }
    return render(request, 'pages/delete_customer.html', context)


# user-side view
# ----------------------------------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def order_details(request, pk):
    order = Order.objects.get(id=pk)
    context = {
        'order': order,
    }
    return render(request, 'pages/user_side/order_details.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def cancel_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('user-page')

    context = {
        'order': order,
    }
    return render(request, 'pages/user_side/cancel_order.html', context)

# ----------------------------------------------


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
    
    customer = Customer.objects.get(id=pk)
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')

    context = {
        'formset': formset,
    }

    return render(request, 'pages/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)  # Get order by id
    form = OrderForm(instance=order) # Create form with order instance

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order) 
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form,
    }

    return render(request, 'pages/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('home')

    context = {
        'item': order,
    }

    return render(request, 'pages/delete_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_all_orders(request):
    orders = Order.objects.all()
    if request.method == 'POST':
        orders.delete()
        return redirect('home')

    context = {
        'orders': orders,
    }

    return render(request, 'pages/delete_all_orders.html', context)







