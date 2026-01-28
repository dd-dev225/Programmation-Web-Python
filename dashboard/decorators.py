from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from functools import wraps


def group_required(*group_names):
    """
    Décorateur vérifiant l'appartenance à un ou plusieurs groupes.
    L'utilisateur doit appartenir à AU MOINS UN des groupes listés.
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            user_groups = request.user.groups.values_list('name', flat=True)
            
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            if any(group in user_groups for group in group_names):
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied("Vous n'avez pas les permissions nécessaires.")
        
        return wrapper
    return decorator


def admin_required(view_func):
    """
    Décorateur spécifique pour les administrateurs uniquement.
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        is_admin = (
            request.user.is_superuser or 
            request.user.groups.filter(name='Administrateurs').exists()
        )
        
        if is_admin:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied("Accès réservé aux administrateurs.")
    
    return wrapper
