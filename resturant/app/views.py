from django.shortcuts import render, get_object_or_404, redirect

from .models import *
from cart.models import *
from cart.views import _cart_id
import datetime


from django.db.models import Q
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

# Create your views here.

def home(request):
    dishes = Dishes_model.objects.all()

    context = {
        'dishes': dishes
    }
    return render(request,'pages/home.html', context)


def products_by_categories(request , category_slug):
    categories  = get_object_or_404(Category, slug=category_slug)
    dishes    = Dishes_model.objects.filter(category=categories,is_available=True)
    product_count = dishes.count()

    filtered_dishes = []
    dishes_variation = []
    up_price = False

    for dish in dishes:
        variations = Variation.objects.filter(dish=dish)
        for variation in variations:
            dishes_variation.append(variation)
            
    if 'filter_price' in request.GET:
        filter_price = request.GET['filter_price']
        def get_price(variation):
            return variation.price
        dishes_variation = list(dishes_variation)
        dishes_variation.sort(key=get_price)
        if str(filter_price) == '1':
            up_price = True
            print(dishes_variation)
            for variation in dishes_variation:
                dish = Dishes_model.objects.get(variation__id=variation.id)
                filtered_dishes.append(dish)
            filtered_dishes = set(filtered_dishes)
            dishes = list(filtered_dishes)
            # dishes.reverse()

        elif str(filter_price) == '2':
            up_price = False
            dishes_variation.reverse()
            for variation in dishes_variation:
                # def get_price(variation):
                #     return variation.price
                # dishes_variation = dishes_variation.sort(key=get_price)
                dish = Dishes_model.objects.get(variation__id=variation.id)
                filtered_dishes.append(dish)
            filtered_dishes = set(filtered_dishes)
            dishes = list(filtered_dishes)
            dishes.reverse()
        product_count = len(dishes)
    

    context = {
        'category_slug': category_slug,
        'up_price': up_price,
        'dishes': dishes,
        'product_count': product_count
    }
    return render(request,'pages/search_page.html', context)


def search_page(request):
    if 'query' in request.GET:
        keyword = request.GET["query"]
        if keyword:
            dishes = Dishes_model.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(slug__icontains=keyword) | Q(dish_name__icontains=keyword) | Q(ingredients__icontains=keyword))
            product_count   = dishes.count()
    else: 
        dishes = None

    context = {
        'keyword': keyword,
        'dishes': dishes,
        'product_count': product_count
    }
    return render(request,'pages/search_page.html', context)

def search_filter(request, keyword):
    dishes = Dishes_model.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(slug__icontains=keyword) | Q(dish_name__icontains=keyword) | Q(ingredients__icontains=keyword))
    filtered_dishes = []
    dishes_variation = []
    up_price = False

    for dish in dishes:
        variations = Variation.objects.filter(dish=dish)
        for variation in variations:
            dishes_variation.append(variation)

    if 'filter_price' in request.GET:
        filter_price = request.GET['filter_price']
        def get_price(variation):
            return variation.price
        dishes_variation = list(dishes_variation)
        dishes_variation.sort(key=get_price)
        if str(filter_price) == '1':
            up_price = True
            print(dishes_variation)
            for variation in dishes_variation:
                dish = Dishes_model.objects.get(variation__id=variation.id)
                filtered_dishes.append(dish)
            filtered_dishes = set(filtered_dishes)
            dishes = list(filtered_dishes)
            # dishes.reverse()

        elif str(filter_price) == '2':
            up_price = False
            dishes_variation.reverse()
            for variation in dishes_variation:
                # def get_price(variation):
                #     return variation.price
                # dishes_variation = dishes_variation.sort(key=get_price)
                dish = Dishes_model.objects.get(variation__id=variation.id)
                filtered_dishes.append(dish)
            filtered_dishes = set(filtered_dishes)
            dishes = list(filtered_dishes)
            dishes.reverse()
        product_count = len(dishes)
    


    context = {
        'keyword': keyword,
        'up_price': up_price,
        'dishes': dishes,
        'product_count': product_count
    }
    return render(request,'pages/search_page.html', context)

def dish_detail(request, id):
    dish  = Dishes_model.objects.get(id=id)
    reviews = ReviewRating.objects.all().filter(dish=dish)
    photos = Dish_gallery.objects.all().filter(dish=dish)
    context = {
        'dish': dish,
        'reviews': reviews,
        'photos': photos
    }
    return render(request,'pages/dish_detail.html', context)




def login(request):
    user = None

    if request.method=="POST":
        if 'email' in request.POST:
            email = request.POST['email']
            user = User.objects.get(email=email)
            password = request.POST['password']
            user = authenticate(username=user.username, password=password)

        if user is not None:
            try:
                cart= Cart.objects.get(cart_id=_cart_id(request))
                cart_item_exists= Cart_item.objects.filter(cart=cart).exists()
                product_variation=[]
                ex_var_list = []
                id = []
                if cart_item_exists:
                    cart_item = Cart_item.objects.filter(cart=cart)
                    # getting the product variation by cart id
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    cart_item = Cart_item.objects.all().filter(user= user)
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index   = ex_var_list.index(pr)
                            item_id = id[index]
                            item = Cart_item.objects.get(id=item_id)
                            item.quantity +=1
                            item.user = user
                            item.save()
                        else :
                            cart_item = Cart_item.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            
            except:
                pass

            auth.login(request, user)
            messages.success(request,"login successful")
            url = request.META.get('HTTP_REFERER')
            return redirect('home')

        else:
            messages.error(request,"invalid credentials!")
            return redirect('login')

    return render(request,'pages/login.html')

def register(request):
    return render(request,'pages/register.html')

@login_required(login_url="login")
def logout(request):

    auth.logout(request)
    messages.success(request,"You are logged out.")

    return redirect('login')



def place_order(request , total =0, quantity = 0):
    current_user = request.user
 
    cart_items = Cart_item.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0 :
        return redirect('store')
    print("works")
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2*total)/100
    grand_total = total + tax
    print("works1")
    
    if request.method == 'POST':
        form = Orderform(request.POST)
        print(form)
        print("works2")

        if form.is_valid():
            data=Order()
            data.user = current_user
            data.first_name= form.cleaned_data['first_name']
            data.last_name= form.cleaned_data['last_name']
            data.email= form.cleaned_data['email']
            data.phone_number= form.cleaned_data['phone_number']
            data.address1= form.cleaned_data['address1']
            data.address2= form.cleaned_data['address2']
            data.city= form.cleaned_data['city']
            data.state= form.cleaned_data['state']
            data.country= form.cleaned_data['country']
            data.order_note= form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            print("works3")

            # generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date+str(data.id)
            data.order_number = order_number
            data.save()
            print("works4")

            order = Order.objects.get(user = current_user, is_ordered=False,order_number= order_number)

            context={
                'quantity':quantity,
                'grand_total':grand_total,
                'total':total,
                'tax':tax,
                'order': order,
                'cart_items':cart_items,
            }
            return render(request,'order/payments.html', context)
    else:
        print("works5")

        return redirect('checkout')