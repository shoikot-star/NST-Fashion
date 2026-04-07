import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Product, Cart, CartItem, Order, OrderItem

# --- HOME & PRODUCT VIEWS ---
def home(request):
    query = request.GET.get('search')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products
    })

# --- CART SYSTEM ---
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.all()
    return render(request, 'cart.html', {'cart': cart, 'items': items})

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')

# --- CHECKOUT & PAYMENT SYSTEM ---
@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        if not cart.cartitem_set.exists():
            return redirect('home')
    except Cart.DoesNotExist:
        return redirect('home')

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        tran_id = str(uuid.uuid4())[:10]
        
        # 1. Order Create
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            phone_number=request.POST.get('phone_number'),
            city=request.POST.get('city'),
            address=request.POST.get('address'),
            total_price=cart.get_total_price(),
            transaction_id=tran_id,
            status='Pending'
        )

        # 2. Transfer Cart Items to Order Items
        for item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity
            )

        # 3. Handle Payment Method
        if payment_method == 'COD':
            order.payment_status = 'Pending (COD)'
            order.save()
            cart.cartitem_set.all().delete()
            return render(request, 'payment_success.html', {'tran_id': 'COD-' + tran_id})

        else:
            # Online Payment (SSLCommerz)
            store_id = 'testbox' 
            store_pass = 'qwerty'
            mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=store_pass)
            
            status_url = request.build_absolute_uri('/payment-status/')
            mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)
            
            mypayment.set_product_integration(
                total_amount=float(order.total_price), 
                currency='BDT', 
                product_category='Fashion', 
                product_name='NST Clothing', 
                num_of_item=1, 
                shipping_method='Courier', 
                product_profile='general'
            )
            
            mypayment.set_customer_info(
                name=order.full_name, 
                email=request.user.email, 
                address1=order.address, 
                city=order.city, 
                postcode='1000', 
                country='Bangladesh', 
                phone=order.phone_number
            )
            
            response = mypayment.init_payment()
            if response['status'] == 'SUCCESS':
                cart.cartitem_set.all().delete()
                return redirect(response['GatewayPageURL'])
            else:
                return render(request, 'payment_failed.html', {'error': response.get('failedreason')})

    return render(request, 'checkout.html', {'cart': cart})

@csrf_exempt
def payment_status(request):
    if request.method == 'POST':
        payment_data = request.POST
        status = payment_data.get('status')
        tran_id = payment_data.get('tran_id')
        
        if status == 'VALID':
            order = get_object_or_404(Order, transaction_id=tran_id)
            order.payment_status = 'Paid'
            order.status = 'Processing'
            order.save()
            return render(request, 'payment_success.html', {'tran_id': tran_id})
        else:
            return render(request, 'payment_failed.html')
            
    return redirect('home')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

# --- AUTH SYSTEM ---
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
def home(request):
    query = request.GET.get('search')
    category_filter = request.GET.get('category') # Category filter-er jonno input nibe
    
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)
    
    if category_filter:
        products = products.filter(category=category_filter) # Category mil thakle filter korbe
        
    return render(request, 'home.html', {'products': products})
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def order_history(request):
    # Shudhu login kora user-er order gulo anbe, latest gulo upore thakbe
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile # Profile model import kora thaka chai

@login_required
def profile_view(request):
    # 'get_or_create' bebohar korle jodi profile na thake, tobe Django sheti toiri kore nibe
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # User details update
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        
        # Profile details update
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.city = request.POST.get('city')
        profile.zip_code = request.POST.get('zip_code')
        profile.save()
        
        return redirect('profile')
        
    return render(request, 'profile.html', {'profile': profile})