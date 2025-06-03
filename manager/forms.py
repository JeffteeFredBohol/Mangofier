from django import forms

class ConfirmSaleForm(forms.Form):
    stock_id = forms.IntegerField(label="Stock ID")
    quantity_sold = forms.IntegerField(min_value=1, label="Quantity Sold")
