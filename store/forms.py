from django import forms
from .models import Quantity, Order

class quantityForm(forms.ModelForm):
    class Meta:
        model = Quantity
        fields = ['quantity']
    
class checkoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address']