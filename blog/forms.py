from django import forms
#...    
class BlogForm(forms.Form):
    product_name = forms.CharField(label='Product Name')  
    product_details = forms.CharField(label='Product Details')  

class form(forms.Form):
    product_name = forms.CharField(label='Product Name')  
    product_details = forms.CharField(label='Product Details')  

	
#...    