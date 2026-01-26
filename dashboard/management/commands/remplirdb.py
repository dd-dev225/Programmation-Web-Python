import csv
from django.core.management.base import BaseCommand
from dashboard.models import Client, Localite, Produit, Commande, Ligne   # ← change 'dashboard' si ton app s'appelle autrement

class Command(BaseCommand):
    help = 'Remplit la table Ligne à partir du fichier CSV (partie 2)'

    def handle(self, *args, **options):
        print('Bonjour ! Début de l\'enregistrement des lignes de commande (partie 2)...')

        lignes = []
        csv_path = "DjangoProject/data/data_bd.csv"

        try:
            with open(csv_path, "rt", encoding="utf-8") as data:
                d = csv.DictReader(data, delimiter=";")
                for row in d:
                    lignes.append(row)
        except UnicodeDecodeError:
            # Si utf-8 échoue, on essaie cp1252 (Windows français)
            print("Encodage utf-8 non reconnu → essai avec cp1252...")
            with open(csv_path, "rt", encoding="cp1252") as data:
                d = csv.DictReader(data, delimiter=";")
                for row in d:
                    lignes.append(row)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Fichier non trouvé : {csv_path}"))
            return

        print(f"{len(lignes)} lignes lues dans le CSV.")

        # =====================================================================
        # PARTIE 1 : création des entités uniques
        # =====================================================================
        print("Partie 1 : création des entités uniques")
        prod_enr = set()
        clt_enr = set()
        loc_enr = set()
        com_enr = set()

        for row in lignes:
            # Localité
            if row['Code_postal'] not in loc_enr:
                Localite.objects.get_or_create(
                    locCodePostal=row['Code_postal'],
                    defaults={
                        'locVille': row['Ville'],
                        'locEtat': row['Etat'],
                        'locRegion': row['Region']
                    }
                )
                loc_enr.add(row['Code_postal'])

            # Client
            if row['ID_Client'] not in clt_enr:
                Client.objects.get_or_create(
                    cltId=row['ID_Client'],
                    defaults={
                        'cltNom': row['Nom_Client'],
                        'cltSegment': row['Segment']
                    }
                )
                clt_enr.add(row['ID_Client'])

            # Produit
            if row['ID_Produit'] not in prod_enr:
                Produit.objects.get_or_create(
                    prodId=row['ID_Produit'],
                    defaults={
                        'prodNom': row['Nom_Produit'],
                        'prodCategorie': row['Categorie'],
                        'prodSousCategorie': row['Sous_Categorie']
                    }
                )
                prod_enr.add(row['ID_Produit'])

            # Commande
            if row['ID_Commande'] not in com_enr:
                Commande.objects.get_or_create(
                    comID=row['ID_Commande'],
                    defaults={
                        'comDate': row['Date_Commande'],
                        'comDateLivraison': row['Date_Livraison'],
                        'comModeLivraison': row['Mode_Livraison']
                    }
                )
                com_enr.add(row['ID_Commande'])

        # =====================================================================
        # PARTIE 2 ACTIVE : création des lignes de commande
        # =====================================================================
        lignes_creees = 0
        erreurs = 0

        for row in lignes:
            try:
                r_commande = Commande.objects.get(comID=row['ID_Commande'])
                r_produit  = Produit.objects.get(prodId=row['ID_Produit'])
                r_client   = Client.objects.get(cltId=row['ID_Client'])
                r_localite = Localite.objects.get(locCodePostal=row['Code_postal'])

                Ligne.objects.create(
                    ligQuantite=int(row['Quantite']),
                    ligPrix=float(row['Ventes'].replace(',', '.')),
                    ligRemise=float(row['Remise'].replace(',', '.')),
                    ligBenefice=float(row['Benefice'].replace(',', '.')),
                    commande=r_commande,
                    produit=r_produit,
                    client=r_client,
                    localite=r_localite
                )

                lignes_creees += 1
                print(f"Ligne créée : commande {row['ID_Commande']} - produit {row['ID_Produit']}")

            except Commande.DoesNotExist:
                print(f"Erreur : Commande {row['ID_Commande']} introuvable")
                erreurs += 1
            except Produit.DoesNotExist:
                print(f"Erreur : Produit {row['ID_Produit']} introuvable")
                erreurs += 1
            except Client.DoesNotExist:
                print(f"Erreur : Client {row['ID_Client']} introuvable")
                erreurs += 1
            except Localite.DoesNotExist:
                print(f"Erreur : Localité {row['Code_postal']} introuvable")
                erreurs += 1
            except Exception as e:
                print(f"Erreur inconnue pour la ligne : {e}")
                erreurs += 1

        print(f"\nRésultat final :")
        print(f"   - Lignes créées : {lignes_creees}")
        print(f"   - Erreurs rencontrées : {erreurs}")

        if erreurs == 0:
            self.stdout.write(self.style.SUCCESS('Base de données remplie avec succès !'))
        else:
            self.stdout.write(self.style.WARNING(f'{erreurs} erreurs détectées - vérifiez les messages ci-dessus.'))