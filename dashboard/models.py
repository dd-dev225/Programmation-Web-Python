from django.db import models

# Create your models here.
REGION = [
    ('Central', 'CENTRAL'), ('West', 'WEST'), ('East', 'EAST'), ('South', 'SOUTH')
]
SEGMENT = [
    ('Consumer', 'CONSUMER'), ('Corporate', 'CORPORATE'), ('Home Office', 'HOME OFFICE')
]

CATEGORIE = [
    ('Furniture', 'FURNITURE'),
    ('Office Supplies', 'OFFICE SUPPLIES'),
    ('Technology', 'TECHNOLOGY'),
]


class Client(models.Model):
    cltId = models.CharField(primary_key=True, verbose_name='ID Client', max_length=10)
    cltNom = models.CharField(verbose_name='Nom et Prenom', max_length=200)
    cltSegment = models.CharField(
        verbose_name='Segment',
        max_length=20,                  # ← ajoute ça (ou 50 si tu préfères)
        choices=SEGMENT
    )

    def __str__(self):
        return f'{self.cltId} - {self.cltNom}'


class Localite(models.Model):
    locId = models.AutoField(verbose_name='ID Localite', primary_key=True)
    locCodePostal = models.PositiveIntegerField(verbose_name='Code Postal', unique=True)
    locVille = models.CharField(verbose_name='Ville', max_length=50)
    locEtat = models.CharField(verbose_name='Etat', max_length=50)
    locRegion = models.CharField(verbose_name='Region', max_length=10, choices=REGION)

    class Meta:
        verbose_name = "Localisation du Client"
        ordering = ['locRegion', 'locEtat']

    def __str__(self):
        return f'{self.locCodePostal} - {self.locVille}'


class Produit(models.Model):
    prodId = models.CharField(verbose_name='ID Produit', primary_key=True, max_length=20)
    prodNom = models.CharField(verbose_name='Produit', max_length=255)
    prodCategorie = models.CharField(               # ← change TextField → CharField
        verbose_name='Categorie',
        max_length=20,
        choices=CATEGORIE
    )
    prodSousCategorie = models.CharField(verbose_name='Sous-Categorie', max_length=50)

    def __str__(self):
        return self.prodNom


class Commande(models.Model):
    comID = models.CharField(verbose_name='Commande', primary_key=True, max_length=20)
    comDate = models.DateField(verbose_name='Date Commande')
    comDateLivraison = models.DateField(verbose_name='Date Livraison')
    comModeLivraison = models.CharField(verbose_name='Mode Livraison', max_length=30)
    comproduits = models.ManyToManyField(Produit, through='Ligne', related_name='contenir', blank=True,
                                         verbose_name="Produits")

    def __str__(self):
        return self.comID


class Ligne(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='commande_produits')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='commande_produits')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='ligne_client')
    localite = models.ForeignKey(Localite, on_delete=models.CASCADE, related_name='ligne_localite')
    ligQuantite = models.IntegerField(verbose_name='Quantité')
    ligPrix = models.FloatField(verbose_name='Prix')
    ligRemise = models.FloatField(verbose_name='Remise', default=0)
    ligBenefice = models.FloatField(verbose_name='Benefice', default=0)

    class Meta:
        ordering = ['produit']
        verbose_name = "Ligne de Commande"

    def __str__(self):
        return f'{self.commande.comID} - {self.client.cltId} - {self.produit.prodId} - {self.ligQuantite} - {self.ligPrix}'


