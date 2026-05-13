from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages, sessions
from .models import Product, Order, OrderItem, Category
from .forms import quantityForm, checkoutForm

# Create your views here.
def home(request):
    latest_products = Product.objects.all().order_by("-created_at")
    popular_products = Product.objects.filter(is_featured=True).order_by("-created_at")[:1]
    featured_products = Product.objects.filter(is_featured=True).order_by("-created_at")
    return render(request, 'home.html', {
        "latest_products": latest_products,
        "popular_products": popular_products,
        "featured_products": featured_products
    })


def store(request):
    products = Product.objects.all().order_by("-created_at")
    return render(request, 'store.html', {"products": products})

def produit_detail(request, pk):
    details = get_object_or_404(Product, pk=pk)
    return render(request, 'produit_detail.html', {"product": details})


def cart(request):
    cart = request.session.get("cart", {})

    cart_items = []
    cart_total = 0
    cart_count = 0

    for product_id , quantity in cart.items():
        try:
            product = Product.objects.get(pk=product_id)
            
            total_price = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': total_price,
            })
            cart_total += total_price
            cart_count += quantity
            
        except Product.DoesNotExist:
            continue
    
    return render(request, 'cart.html', {
        "cart_items": cart_items,
        "cart_total": cart_total,
        "cart_count": cart_count
    })

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get("cart", {})

        item_id = str(pk)

        current_quantity = cart.get(item_id, 0)

        if (current_quantity + quantity) <= product.stock:
            cart[item_id] = current_quantity + quantity
            request.session["cart"] = cart
            request.session.modified = True
        else:
            messages.error(request, message="Stock insuffisant !")
    
    return redirect('cart')

def reduce_quantity(request, pk):
    item_id = str(pk)
    cart = request.session.get("cart", {})

    current_quantity = cart.get(item_id, 0)

    if current_quantity > 1:
        cart[item_id] = current_quantity - 1
    else:
        cart.pop(item_id, None)

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def increase_quantity(request, pk):
    item_id = str(pk)
    product = get_object_or_404(Product, pk=pk)

    cart = request.session.get("cart", {})

    current_quantity = cart.get(item_id, 0)

    if current_quantity < product.stock:
        cart[item_id] = current_quantity + 1
    else:
        messages.error(request, "Quantité maximale disponible atteinte.")

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def delete_product(request, pk):
    item_id = str(pk)
    cart = request.session.get("cart", {})

    cart.pop(item_id, None)

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


from django.db import transaction 

def checkout(request):
    cart = request.session.get("cart", {})
    cart_items = []
    cart_total = 0
    cart_count = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            stock = product.stock
            if quantity <= stock:
                total_price = product.price * quantity
                cart_items.append({
                    "product": product,
                    "quantity": quantity,
                    "total_price": total_price,
                })
                cart_total += total_price
                cart_count += quantity
            else:
                messages.error(request, f"Stock insuffisant pour {product.name}.")
                return redirect("cart")
        except Product.DoesNotExist:
            continue 

    if not cart_items:
        messages.error(request, "Votre panier est vide.")
        return redirect("cart")

    if request.method == "POST":
        form = checkoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.total_price = cart_total
                    order.save()

                    for item in cart_items:
                        product = item["product"]
                        qty = item["quantity"]

                        if product.stock >= qty:
                            product.stock -= qty
                            if product.stock == 0:
                                product.is_available = False
                            product.save()
                        else:
                            raise Exception(f"Stock insuffisant pour {product.name}")

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=qty,
                            price=product.price,
                        )

                    request.session["cart"] = {}
                    request.session.modified = True

                    messages.success(request, "Merci pour votre commande !")
                    return redirect("checkout_success")
            
            except Exception as e:
                messages.error(request, f"Erreur lors de la validation : {str(e)}")
                return redirect("checkout")
    else:
        form = checkoutForm()

    return render(request, 'checkout.html', {
        "form": form,
        "cart_items": cart_items,
        "cart_total": cart_total,
        "cart_count": cart_count,
    })

def checkout_success(request):
    request.session["cart"] = {}
    request.session.modified = True
    return render(request, 'checkout_success.html')

def products_by_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category)

    categories = Category.objects.all()

    if category:
        active_category = category
    else:
        active_category = None
    return render(request, 'categories.html', {
        "products": products,
        "categories": categories,
        "active_category": active_category
        })

def categories(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    return render(request, 'categories.html', {
        "products": products,
        "categories": categories,
        })













# def cart(request):
#     cart = request.session.get("cart", {})    
#     cart_items = []
#     cart_total = 0
#     cart_count = 0


#     for product_id, quantity in cart.items():
#         product = get_object_or_404(Product, pk=product_id)
#         total_price = product.price * quantity
#         cart_items.append({
#             'product': product,
#             'quantity': quantity,
#             'total_price': total_price,
#         })
#         cart_total += total_price
#         cart_count += quantity

#     return render(request, 'cart.html', {
#         'cart_items': cart_items,
#         'cart_total': cart_total,
#         'cart_count': cart_count
#         })

# def add_to_cart(request, pk, quantity=1): # 1 est plus standard que 2
#     product = get_object_or_404(Product, pk=pk)
#     cart = request.session.get("cart", {})
    
#     item_id = str(pk)
    
#     if item_id in cart:
#         cart[item_id] += quantity
#     else:
#         cart.update({item_id: quantity})
    
#     request.session["cart"] = cart
#     request.session.modified = True

#     return redirect('cart')