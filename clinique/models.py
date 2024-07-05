from datetime import datetime
from django.db import models
from django.forms import ValidationError
from django.core.exceptions import ValidationError
from django.db.models import Sum





# Create your models here.
class Member(models.Model):
    firstname =  models.CharField(max_length=100)
    lastname = models.CharField(max_length=50)
    
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    quantite_stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    
    def sell(self, quantite):
        if self.quantite_stock >= quantite:
            self.quantite_stock -= quantite
            self.save()
            return True
        return False
    def __str__(self):
        return self.name

class Vente(models.Model):
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantite_vente = models.IntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    prix_de_vente = models.DecimalField(max_digits=10, decimal_places=2)
    date_vente = models.DateTimeField(auto_now_add=True)

    def calculer_benefice(self):
        return self.prix_de_vente - self.prix_unitaire


class PatientConsultation(models.Model):
    patient_id=models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    date_consultation = models.DateField()
    STATUT_CHOICES = [
        ('consulte', 'Consulté'),
        ('hospitalise', 'Hospitalisé'),
        ('examine', 'Examiné'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)

    def __str__(self):
        return self.nom

    
    def clean(self):
        # Vérifiez si le statut est "hospitalise" et que la date de consultation est définie
        if self.statut == 'hospitalise' and not self.date_consultation:
            raise ValidationError("La date de consultation doit être définie pour un patient hospitalisé.")

        # Vérifiez si le statut est "hospitalise" et que le statut précédent est "consulte"
        if self.statut == 'hospitalise':
            previous_consultations = PatientConsultation.objects.filter(nom=self.nom, statut='consulte')
            if not previous_consultations.exists():
                raise ValidationError("Un patient ne peut être hospitalisé que s'il a déjà été consulté.")

        super().clean()
        
        @classmethod
        def generer_rapport(cls):
            mois_en_cours = datetime.now().replace(day=1)
            mois_formatte = mois_en_cours.strftime("%m/%Y")

            patients_consultes = cls.objects.filter(statut='consulte').count()
            patients_hospitalises = cls.objects.filter(statut='hospitalise').count()
            patients_examines = cls.objects.filter(statut='examine').count()

            ventes_mois_en_cours = Vente.objects.filter(date_vente__month=mois_en_cours.month)
            montant_ventes = ventes_mois_en_cours.aggregate(Sum('prix_de_vente'))['prix_de_vente__sum'] or 0

            benefice_realise = Sum(vente.calculer_benefice() for vente in ventes_mois_en_cours)

            rapport, created = cls.objects.get_or_create(
                mois=mois_formatte,
                defaults={
                    'patients_consultes': patients_consultes,
                    'patients_hospitalises': patients_hospitalises,
                    'patients_examines': patients_examines,
                    'montant_ventes': montant_ventes,
                    'benefice_realise': benefice_realise,
                }
            )

            return rapport, mois_formatte
        
        
class Salle(models.Model):
    nouvelle_salle_id=models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    capacite_max = 5
    patients_actuels = models.PositiveIntegerField(default=0)
    patients = models.ManyToManyField(PatientConsultation)

    def est_pleine(self):
        return self.patients_actuels >= self.capacite_max
    def ajouter_patient(self,patient):
        """
        Ajoute un patient à la salle.
        """
        if not self.est_pleine():
            self.patients.add(patient)
            self.patients_actuels += 1
            self.save()
            return True
        else:
            return False

   

    def __str__(self):
        return self.nom

        
class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,default='0')

    def save(self, *args, **kwargs):
        if self.product.sell(self.quantity):
            super().save(*args, **kwargs)
        else:
            raise ValueError("Pas assez de stock pour la vente")



