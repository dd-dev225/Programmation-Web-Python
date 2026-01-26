from django.shortcuts import render
from .models import *
from django.db.models import Sum
import plotly.express as px
import pandas as pd



# Comment  récuperer les information de la table de donnée pour les afficher dans une page
# Recherhce sur comment on fait les requêtes sur Django
# Comment est ce qu'on gère les urls
# Enregistrer les données.
# Comment est ce qu'on intègre le contenu d'un templates.
# Comment injecter les donénes récupérer dans notrees vues pour avoir ce qu'on veut .


# Create your views here.
def dashboard_2(request):
    nb_client = Client.objects.all().count()
    qs = Produit.objects.all().values
    nb_prod = Produit.objects.all().count()
    context = {
        "message": 'La vie est belle !'
        # Définir ici toutes les variable à transférer à la page html
    }
    return render(request, "dashboard/dashboard_2.html", context)

def segmentliste(request, segment):
    query_set = Ligne.objects.filter(client__cltSegment=segment)
    context = {
        'query_set': query_set,
    }
    return render(request, "dashboard/listes_data_segment.html", context)
def dashboard_1(request):
    total_vente = Ligne.objects.filter(client__cltSegment="Consumer").aggregate(ca_seg=Sum("ligPrix"))
    data = Ligne.objects.values('localite__locRegion', 'ligQuantite', 'localite__locVille')
    df_data = pd.DataFrame(data)

    # Construction de la figure 1 avec plotly express
    # Nombre de produits vendus par région
    fig = px.pie(df_data, values='ligQuantite', names='localite__locRegion',
                 color_discrete_sequence=['#FCC6BB', '#F87C63', '#C82909', '#701705'],
                 labels={'ligQuantite': 'Nombre de produits', 'localite__locRegion': 'Région'})
    fig.update_traces(textposition='inside', textinfo='percent+label', hovertemplate=None,
                      hoverinfo='skip', showlegend=False)
    chart = fig.to_html()
    context = {
        # Définir ici toutes les variable à transférer à la page html
        'total_vente': round(total_vente['ca_seg'], 2),
        'chart': chart
    }
    return render(request, "dashboard/dashboard_1.html", context)