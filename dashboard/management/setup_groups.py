"""
Script pour créer les groupes et utilisateurs de test
Exécuter via: python manage.py shell < dashboard/management/setup_groups.py
Ou copier-coller le contenu dans le shell Django
"""
from django.contrib.auth.models import Group, Permission, User

print("=" * 50)
print("CRÉATION DES GROUPES ET UTILISATEURS")
print("=" * 50)

# Création des groupes
administrateurs, created = Group.objects.get_or_create(name='Administrateurs')
print(f"Groupe Administrateurs: {'créé' if created else 'existait déjà'}")

utilisateurs_standard, created = Group.objects.get_or_create(name='Utilisateurs Standard')
print(f"Groupe Utilisateurs Standard: {'créé' if created else 'existait déjà'}")

# Attribution des permissions
all_permissions = Permission.objects.all()
view_permissions = Permission.objects.filter(codename__startswith='view_')

administrateurs.permissions.set(all_permissions)
utilisateurs_standard.permissions.set(view_permissions)

print(f"\nAdministrateurs: {administrateurs.permissions.count()} permissions")
print(f"Utilisateurs Standard: {utilisateurs_standard.permissions.count()} permissions")

# Création utilisateur admin_test
if not User.objects.filter(username='admin_test').exists():
    admin_user = User.objects.create_user(
        username='admin_test',
        email='admin@test.com',
        password='Admin@123',
        first_name='Admin',
        last_name='Test'
    )
    admin_user.is_staff = True
    admin_user.save()
    admin_user.groups.add(administrateurs)
    print("\nUtilisateur admin_test créé (mdp: Admin@123)")
else:
    print("\nUtilisateur admin_test existe déjà")

# Création utilisateur user_test
if not User.objects.filter(username='user_test').exists():
    standard_user = User.objects.create_user(
        username='user_test',
        email='user@test.com',
        password='User@123',
        first_name='User',
        last_name='Test'
    )
    standard_user.groups.add(utilisateurs_standard)
    print("Utilisateur user_test créé (mdp: User@123)")
else:
    print("Utilisateur user_test existe déjà")

print("\n" + "=" * 50)
print("RÉSUMÉ")
print("=" * 50)
for g in Group.objects.all():
    print(f"{g.name}: {g.permissions.count()} perms, {g.user_set.count()} users")
print("=" * 50)
