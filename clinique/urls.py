from django.urls import path
from . import views

app_name="clinique"

urlpatterns = [
     path('ajouter_patient/', views.ajouter_patient, name='ajouter_patient'),
     path('patient/', views.liste_patient, name='liste_patient'),
     path('add_product/', views.add_product, name='add_product'),
     path('product_list/', views.product_list, name='product_list'),
     path('sell/<int:product_id>/', views.sell_product, name='sell_product'),
     path('vendre/<int:id>/<int:quantite_vendue>/', views.vendre_produit, name='vendre'),
     path('liste_vente/', views.liste_vente, name='liste_vente'),
     path('delete_consultation/<int:patient_id>/', views.delete_consultation, name='delete_consultation'),
     path('patient/<int:patient_id>/modifier/', views.patient_modifier, name='patient_modifier'),
     path('creer_salle/',views.creer_salle, name='creer_salle'),
     path('salle_list/',views.salle_list, name='salle_list'),
     path('salle_ajout_p/<int:nouvelle_salle_id>/', views.salle_ajout_p, name='salle_ajout_p'),
     path('changer_salle_patient/<int:patient_id>/', views.changer_salle_patient, name='changer_salle_patient'),
     path('supprime_salle_p/<int:nouvelle_salle_id>/', views.supprime_salle_p, name='supprime_salle_p'),
     path('salle_detail/<int:nouvelle_salle_id>/', views.salle_detail, name='salle_detail'),
     path('modify_product/<int:product_id>',views.modify_product,name='modify_product'),
     path('delete_product/<int:product_id>/',views.delete_product,name='delete_product'),
     path('sale_list/', views.sale_list, name='sale_list'),
     path('profits/', views.calculate_profits, name='profits'),
     path('', views.index,name="index"),
     path('rapport_par_mois/', views.rapport_par_mois, name='rapport_par_mois'),
     path('annuler_vente/<int:sale_id>/', views.annuler_vente, name='annuler_vente'),
     
]
