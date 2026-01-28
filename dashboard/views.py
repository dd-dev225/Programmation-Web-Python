from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime
import plotly.express as px
import pandas as pd

from .models import Client, Produit, Ligne, Localite
from .decorators import group_required, admin_required


# ═══════════════════════════════════════════════════════════════
# DASHBOARDS - Accessibles aux Administrateurs ET Utilisateurs Standard
# ═══════════════════════════════════════════════════════════════

@login_required
@group_required('Administrateurs', 'Utilisateurs Standard')
def dashboard_1(request):
    """Dashboard principal avec graphique des ventes par région"""
    ca_consumer = Ligne.objects.filter(client__cltSegment="Consumer").aggregate(ca_seg=Sum("ligPrix"))
    data = Ligne.objects.values('localite__locRegion', 'ligQuantite', 'localite__locVille')
    df_data = pd.DataFrame(data)

    # Graphique camembert avec Plotly
    fig = px.pie(df_data, values='ligQuantite', names='localite__locRegion',
                 color_discrete_sequence=['#FCC6BB', '#F87C63', '#C82909', '#701705'],
                 labels={'ligQuantite': 'Nombre de produits', 'localite__locRegion': 'Région'})
    fig.update_traces(textposition='inside', textinfo='percent+label', hovertemplate=None,
                      hoverinfo='skip', showlegend=False)
    chart = fig.to_html()
    
    context = {
        'ca_consumer': round(ca_consumer['ca_seg'], 2) if ca_consumer['ca_seg'] else 0,
        'chart': chart,
        'is_admin': request.user.groups.filter(name='Administrateurs').exists() or request.user.is_superuser,
    }
    return render(request, "dashboard/dashboard_1.html", context)


@login_required
@group_required('Administrateurs', 'Utilisateurs Standard')
def dashboard_2(request):
    """Dashboard secondaire avec statistiques générales"""
    nb_client = Client.objects.all().count()
    nb_prod = Produit.objects.all().count()
    context = {
        "message": 'La vie est belle !',
        "nb_client": nb_client,
        "nb_prod": nb_prod,
        'is_admin': request.user.groups.filter(name='Administrateurs').exists() or request.user.is_superuser,
    }
    return render(request, "dashboard/dashboard_2.html", context)


@login_required
@group_required('Administrateurs', 'Utilisateurs Standard')
def segmentliste(request, segment):
    """Liste des lignes filtrées par segment client"""
    seg_qs = Ligne.objects.filter(client__cltSegment=segment)
    context = {
        'seg_data': seg_qs,
        'is_admin': request.user.groups.filter(name='Administrateurs').exists() or request.user.is_superuser,
    }
    return render(request, "dashboard/listes_data_segment.html", context)


# ═══════════════════════════════════════════════════════════════
# GESTION - Accessibles uniquement aux Administrateurs
# ═══════════════════════════════════════════════════════════════

@login_required
@admin_required
def gestion_utilisateurs(request):
    """Liste et gestion des utilisateurs - ADMIN UNIQUEMENT"""
    # prefetch_related optimise les requêtes pour les groupes
    users = User.objects.all().prefetch_related('groups')
    context = {
        'users': users,
        'is_admin': True,
    }
    return render(request, 'dashboard/gestion_utilisateurs.html', context)


@login_required
@admin_required
def gestion_groupes(request):
    """Liste et gestion des groupes - ADMIN UNIQUEMENT"""
    groups = Group.objects.all().prefetch_related('permissions')
    context = {
        'groups': groups,
        'is_admin': True,
    }
    return render(request, 'dashboard/gestion_groupes.html', context)


# ═══════════════════════════════════════════════════════════════
# AUTHENTIFICATION - Connexion/Déconnexion personnalisées
# ═══════════════════════════════════════════════════════════════

def custom_login(request):
    """Vue de connexion avec variables de session personnalisées"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Création des variables de session personnalisées
            request.session['user_session_data'] = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'groups': list(user.groups.values_list('name', flat=True)),
                'login_time': datetime.now().isoformat(),
                'is_admin': user.groups.filter(name='Administrateurs').exists() or user.is_superuser,
            }
            
            messages.success(request, f'Bienvenue {user.username}!')
            return redirect('dashboard:dashboard_1')
        else:
            messages.error(request, 'Identifiant ou mot de passe incorrect.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'dashboard/login2.html', {'form': form})


def custom_logout(request):
    """Vue de déconnexion avec nettoyage des sessions"""
    username = request.user.username if request.user.is_authenticated else "Utilisateur"
    
    # Nettoyage des variables de session personnalisées
    if 'user_session_data' in request.session:
        del request.session['user_session_data']
    if 'last_activity' in request.session:
        del request.session['last_activity']
    
    logout(request)
    messages.info(request, f'Au revoir {username}!')
    return redirect('dashboard:login')