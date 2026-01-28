from django.utils.deprecation import MiddlewareMixin
from datetime import datetime


class UserSessionMiddleware(MiddlewareMixin):
    """
    Middleware gérant les variables de session personnalisées.
    """
    
    def process_request(self, request):
        if request.user.is_authenticated:
            if 'user_session_data' not in request.session:
                request.session['user_session_data'] = {
                    'user_id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                    'groups': list(request.user.groups.values_list('name', flat=True)),
                    'login_time': datetime.now().isoformat(),
                    'is_admin': (
                        request.user.groups.filter(name='Administrateurs').exists() or 
                        request.user.is_superuser
                    ),
                }
                request.session.modified = True
            
            request.session['last_activity'] = datetime.now().isoformat()
        
        return None
    
    def process_response(self, request, response):
        return response
