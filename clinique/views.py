import datetime
from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.db.models.functions import Round
from clinique.forms import PatientCForm, ProductForm, SaleForm, SalleForm
from clinique.models import Member, PatientConsultation, Product, Sale, Salle, Vente
from django.db.models import Sum
import matplotlib.pyplot as plt # type: ignore
from django.contrib.auth.decorators import login_required,permission_required
from django.db.models.functions import TruncMonth




# Create your views here.

def index(request):
    member=Member.objects.all()
    return render(request,'index.html',{'member':member})
@login_required
def ajouter_patient(request):
    if request.method == 'POST':
        form = PatientCForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clinique:liste_patient')  # Redirigez vers la liste des patients
    else:
        form = PatientCForm()

    return render(request, 'ajouter_patient.html', {'form': form})
@login_required
def liste_patient(request):
    patients = PatientConsultation.objects.all()
    return render(request, 'liste_patient.html', {'patients': patients})
@login_required
def delete_consultation(request, patient_id):
    patient = get_object_or_404(PatientConsultation, pk=patient_id)
    if request.method == 'POST':
        patient.delete()
        # Redirigez vers la page appropriée après la suppression (par exemple, la liste des consultations)
        return redirect('clinique:liste_patient')
    return render(request, 'delete_consultation.html', {'patient': patient})
@login_required
def patient_modifier(request, patient_id):
    patients = PatientConsultation.objects.get(pk=patient_id)

    if request.method == 'POST':
        form = PatientCForm(request.POST, instance=patients)
        if form.is_valid():
            form.save()
            return redirect('clinique:liste_patient')  # Remplacez par le nom de votre vue de liste des patients
    else:
        form = PatientCForm(instance=patients)

    return render(request, 'patient_modifier.html', {'form': form, 'patients': patients})


def statistiques_mensuelles(request):
    # Agrégez les consultations par mois et par statut
    stats_mensuelles = PatientConsultation.objects.annotate(month=ExtractMonth('date_consultation')).values('month', 'statut').annotate(count=Count('id'))

    return render(request, 'statistiques_mensuelles.html', {'stats_mensuelles': stats_mensuelles})

def statistiques_par_statut(request):
    # Agrégez les consultations par statut
    stats_par_statut = PatientConsultation.objects.values('statut').annotate(count=Count('id'))

    return render(request, 'statistiques_par_statut.html', {'stats_par_statut': stats_par_statut})
@login_required
def creer_salle(request):
    if request.method == 'POST':
        form = SalleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clinique:salle_list')  # Redirige vers la liste des salles
    else:
        form = SalleForm()
    return render(request, 'creer_salle.html', {'form': form})


@login_required
def salle_list(request):
    salles = Salle.objects.all()
    return render(request, 'salle_list.html', {'salles': salles})

@login_required
def salle_ajout_p(request, nouvelle_salle_id):
    salle = get_object_or_404(Salle, pk=nouvelle_salle_id)

    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        try:
            patient = PatientConsultation.objects.get(pk=patient_id)
        except PatientConsultation.DoesNotExist:
            return render(request, 'erreur.html', {'message': 'Patient introuvable'})

        if not salle.est_pleine():
            # Ajoutez le patient à la salle
            salle.patients.add(patient)
            salle.patients_actuels += 1
            salle.save()
            # Redirigez vers la page souhaitée
            return redirect('clinique:salle_list')  # Remplacez par le nom de votre vue de liste des salles
        else:
            return render(request, 'erreur.html', {'message': 'La salle est pleine'})

    # Affichez le formulaire pour ajouter un patient à la salle
    patients_disponibles = PatientConsultation.objects.all()
    return render(request, 'salle_ajout_p.html', {'salle': salle, 'patients_disponibles':patients_disponibles})
@login_required
def changer_salle_patient(request,patient_id):
    patient = get_object_or_404(PatientConsultation, pk=patient_id)

    if request.method == 'POST':
        nouvelle_salle_id = request.POST.get('nouvelle_salle')
        salle = get_object_or_404(Salle, pk=nouvelle_salle_id)

        if not salle.est_pleine():
            # Retirez le patient de l'ancienne salle
            patient.salle.patients.remove(patient)
            patient.salle.patients_actuels -= 1
            patient.salle.save()

            # Ajoutez le patient à la nouvelle salle
            salle.patients.add(patient)
            salle.patients_actuels += 1
            salle.save()

            # Redirigez vers la page souhaitée (par exemple, la liste des salles)
            return redirect('clinique:salle_list')  # Remplacez par le nom de votre vue de liste des salles

    # Affichez le formulaire pour changer la salle du patient
    salles_disponibles = Salle.objects.exclude(id=patient.salle.nouvelle_salle.id)
    return render(request, 'changer_patient_salle.html', {'patient': patient, 'salles_disponibles': salles_disponibles})
@login_required
def salle_detail(request, nouvelle_salle_id):
    try:
        salle = Salle.objects.get(pk=nouvelle_salle_id)
    except Salle.DoesNotExist:
        return render(request, 'erreur.html', {'message': 'Salle introuvable'})

    return render(request, 'salle_detail.html', {'salle': salle})

@login_required
def supprime_salle_p(request, nouvelle_salle_id):
    salle = get_object_or_404(Salle, pk=nouvelle_salle_id)

    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        try:
            patient = PatientConsultation.objects.get(pk=patient_id)
        except PatientConsultation.DoesNotExist:
            return render(request, 'erreur.html', {'message': 'Patient introuvable'})

        # Votre logique pour supprimer le patient de la salle ici
        # Par exemple, si vous souhaitez simplement retirer le patient de la salle :
        salle.patients.remove(patient)
        salle.patients_actuels -= 1
        salle.save()

        # Redirigez vers la page souhaitée (par exemple, la liste des salles)
        return redirect('clinique:salle_list')  # Remplacez par le nom de votre vue de liste des salles
    else:
        # Gérez le cas où la salle est pleine
        if salle.patients_actuels <= 0:
            return render(request, 'erreur.html', {'message': 'La salle est déjà vide'})
        else:
            # Affichez le formulaire pour supprimer un patient de la salle
            patients_disponibles = PatientConsultation.objects.all()
            return render(request, 'supprime_salle_p.html', {'salle': salle, 'patients_disponibles': patients_disponibles})
    

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clinique:product_list')  # Assuming you have a product list view
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required
def sell_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.product = product
            if sale.quantity > product.quantite_stock:
                form.add_error('quantity', 'Quantité insuffisante en stock')
            else:
                
                product.save()
                sale.save()
                return redirect('clinique:product_list')
    else:
        form = SaleForm()
    return render(request, 'sell_product.html', {'form': form, 'product': product})
@login_required
def modify_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('clinique:product_list')  # Remplacez par le nom de votre vue de liste des produits
    else:
        form = ProductForm(instance=product)
    return render(request, 'modify_product.html', {'form': form, 'product': product})
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.delete()
        # Redirigez vers la page appropriée après la suppression (par exemple, la liste des consultations)
        return redirect('clinique:product_list')
    return render(request, 'delete_product.html', {'product': product})
@login_required
def sale_list(request):
    sales = Sale.objects.all()  # Récupère toutes les ventes
    return render(request, 'sale_list.html', {'sales': sales})
@login_required
def calculate_profits(request):
    # Récupérez toutes les ventes (vous pouvez filtrer par date, produit, etc.)
    sales = Sale.objects.all()

    # Effectuez les calculs pour obtenir les bénéfices totaux
    total_profits = 0
    for sale in sales:
        product = Product.objects.get(id=sale.product_id)
        total_profits += sale.quantity * product.price

    return render(request, 'profits.html', {'total_profits': total_profits})
@login_required
def liste_vente(request):
    ventes = Vente.objects.all()
    return render(request, 'liste_vente.html', {'ventes': ventes})


@login_required
def vendre_produit(request, produit_id, quantite_vendue):
    produit = get_object_or_404(Product, pk=produit_id)

    if produit.quantite_stock >= quantite_vendue:
        # Mettez à jour la quantité en stock
        produit.quantite_stock -= quantite_vendue
        produit.save()
        message = f"Vente réussie ! Nouvelle quantité en stock : {produit.quantite_stock}"
    else:
        message = "La quantité en stock n'est pas suffisante pour cette vente."

    return render(request, 'votre_template.html', {'message': message})



  
    
@login_required   
def rapport_par_mois(request):
    # Récupérez les données et filtrez par mois et statut
    consultations = PatientConsultation.objects.annotate(month=TruncMonth('date_consultation')).values('month', 'statut').annotate(count=Count('patient_id'))

    # Créez un dictionnaire pour stocker les statistiques par mois et statut
    stats_par_mois = {}
    for consultation in consultations:
        month = consultation['month'].strftime('%Y-%m')
        statut = consultation['statut']
        count = consultation['count']

        if month not in stats_par_mois:
            stats_par_mois[month] = {}

        stats_par_mois[month][statut] = count

    # Passez les données au modèle (template) pour l'affichage
    return render(request, 'rapport_par_mois.html', {'stats_par_mois': stats_par_mois})

@login_required 
def annuler_vente(request, sale_id):
    sale = get_object_or_404(Sale, pk=sale_id)

    if request.method == 'POST':
        # Annulez la vente (par exemple, en remettant la quantité vendue au stock)
        # Vous pouvez ajuster cette logique selon vos besoins

        # Supprimez la vente
        sale.delete()

        return redirect('clinique:sale_list')
        # Remplacez par le nom de votre vue d'historique des ventes

    return render(request, 'annuler_vente.html', {'sale': sale})

