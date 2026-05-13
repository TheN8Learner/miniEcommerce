from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.store, name='store'),
    path('produit_detail/<int:pk>', views.produit_detail, name='produit_detail'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
    path('reduce_quantity/<int:pk>', views.reduce_quantity, name='reduce_quantity'),
    path('increase_quantity/<int:pk>', views.increase_quantity, name='increase_quantity'),
    path('delete_product/<int:pk>', views.delete_product, name='delete_product'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success')

]