from django.shortcuts import render
from django.http import HttpResponse


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegisterForm,ChangeUserData
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm
from .models import Address
from .forms import AddressForm

from .models import Jersi, Cart,Category

from django.core.paginator import Paginator



def home(request):
    jersis = Jersi.objects.all()
    categories = Category.objects.all()

    return render(request, 'base.html', {'jersis': jersis,'categories': categories})


def add_to_cart(request, jersi_id):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        jersi = get_object_or_404(Jersi, id=jersi_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, jersi=jersi)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('cart')
    else:
        messages.success(request, 'You have create an account and go to cart page')
        return redirect('signin')  # Removed extra argument, just redirect to 'signin'
         


def cart(request):
    if request.user.is_authenticated:
        categories = Category.objects.all()
        cart_items = Cart.objects.filter(user=request.user).select_related('jersi__category')
        total_price = sum(item.jersi.price * item.quantity for item in cart_items)
        tax = (2 * total_price) / 100  # 2% VAT
        total_price = total_price + tax
        return render(request, 'cart.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            'tax': tax,
            'categories': categories,
        })
    else:
        messages.success(request, 'You have create an account and go to cart page')
        return redirect('signin')
         


def update_cart(request, cart_item_id, action):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()
            return redirect('cart')
    elif action == 'delete':
        cart_item.delete()
        return redirect('cart')
    
    cart_item.save()
    return redirect('cart')

def jersi_dec_view(request, jersi_id):
    jersi = get_object_or_404(Jersi, id=jersi_id)
    categories = Category.objects.all()
    return render(request, 'jersi_dec.html', {'jersi': jersi, 'categories': categories})



def store(request, category_id=None):
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        jersis = Jersi.objects.filter(category=category)
    else:
        jersis = Jersi.objects.all()

    paginator = Paginator(jersis, 6)
    page = request.GET.get('page')
    paged_jersis = paginator.get_page(page)

    categories = Category.objects.all()
    context = {
        'jersis': paged_jersis,
        'categories': categories,
    }
    return render(request, 'store.html', context)

def search_jersi(request):
    query = request.GET.get('q')
    if query:
        jersis = Jersi.objects.filter(name__icontains=query)
    else:
        jersis = Jersi.objects.all()
    return render(request, 'home.html', {'jersis': jersis})



def checkout(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.jersi.price * item.quantity for item in cart_items)
        tax = (2 * total_price) / 100  # 2% VAT
        total_price_with_tax = total_price + tax

        # Calculate total price for each item
        for item in cart_items:
            item.total_price = item.jersi.price * item.quantity

        if request.method == 'POST':
            form = AddressForm(request.POST)
            if form.is_valid():
                address = form.save(commit=False)
                address.user = request.user
                address.save()
                messages.success(request, 'Your order successfully placed!')
                return redirect('order_complate')
            
        else:
            form = AddressForm()

        return render(request, 'checkout.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            'tax': tax,
            'total_price_with_tax': total_price_with_tax,
            'form': form
        })
    else:
        messages.success(request, 'You need to create an account and log in to proceed to checkout.')
        return redirect('signin')
    
    
def signup(request):
   if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            messages.success(request,' Your Account created successfull!')
            form.save()       
            print(form.cleaned_data)
            return redirect('signin')
   else:
        form = RegisterForm()
   return render(request, 'register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data = request.POST)
        if form.is_valid():
           messages.success(request,' Login successfully!!!')
           name = form.cleaned_data['username']
           userpass = form.cleaned_data['password']
           user = authenticate(username = name,password = userpass)
           if user is not None:
              login(request,user)
              return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html',{'form': form})



def user_logout(request):
    logout(request)
    return redirect('home')



def Profile(request):
     if request.user.is_authenticated:
       return render(request, 'dashboard.html')
     else:
         messages.success(request,'You have create an account and go to dashboard page')
         return redirect( 'signin')


def order_complete(request):
  if request.user.is_authenticated: 
    user = request.user
    address = Address.objects.filter(user=user).last()
    cart_items = Cart.objects.filter(user=user)
    
    total_price = sum(item.jersi.price * item.quantity for item in cart_items)
    tax = (2 * total_price) / 100  # 2% VAT
    total_price_with_tax = total_price + tax

    return render(request, 'order_complate.html', {
        'user': user,
        'address': address,
        'cart_items': cart_items,
        'total_price': total_price,
        'tax': tax,
        'total_price_with_tax': total_price_with_tax
    })
  else:
    messages.success(request,'You have create an account and go to order_complate page')
    return redirect( 'signin')