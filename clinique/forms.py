from django import forms
from .models import PatientConsultation, Product, Sale, Salle


class PatientCForm(forms.ModelForm):
    class Meta:
        model = PatientConsultation
        fields = ['nom', 'date_consultation', 'statut']
        
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'quantity']
        

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantite_stock','price']
        
class SalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        fields = ['nom']