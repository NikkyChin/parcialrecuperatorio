# parcialrecuperatorio

A continuación, te proporciono los pasos y el script solicitado para cumplir con los requisitos:

Configurar el archivo settings.py para producción
DEBUG: Establecerlo en False.
ALLOWED_HOSTS: Definir los dominios permitidos (por ejemplo: ['tu_dominio.com']).
STATIC_ROOT: Configurar la ruta para servir archivos estáticos.
Ejemplo:

python
Copiar código
DEBUG = False
ALLOWED_HOSTS = ['tu_dominio.com']
STATIC_ROOT = BASE_DIR / 'staticfiles'
Script para crear grupos, permisos y usuarios
El siguiente script crea los grupos, asigna permisos y usuarios de acuerdo a lo solicitado:

python
Copiar código
import os
import django

# Configura el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')
django.setup()

from django.contrib.auth.models import Group, Permission, User
from mensajes.models import Mensaje
from django.contrib.contenttypes.models import ContentType

# Crear permisos personalizados
content_type = ContentType.objects.get_for_model(Mensaje)

perm_crear = Permission.objects.create(
    codename='crear_perm',
    name='Puede crear mensajes',
    content_type=content_type,
)

perm_ver = Permission.objects.create(
    codename='ver_perm',
    name='Puede ver mensajes',
    content_type=content_type,
)

perm_borrar = Permission.objects.create(
    codename='borrar_perm',
    name='Puede borrar mensajes',
    content_type=content_type,
)

# Crear grupos y asignar permisos
grupo_creador = Group.objects.create(name='Creador')
grupo_creador.permissions.add(perm_crear)

grupo_editor = Group.objects.create(name='Editor')
grupo_editor.permissions.add(perm_ver, perm_borrar)

grupo_admin = Group.objects.create(name='Administrador')
grupo_admin.permissions.add(perm_crear, perm_ver, perm_borrar)

# Crear usuarios y asignarles grupos
usuario1 = User.objects.create_user(username='creador', password='password123')
usuario1.groups.add(grupo_creador)

usuario2 = User.objects.create_user(username='editor', password='password123')
usuario2.groups.add(grupo_editor)

usuario3 = User.objects.create_user(username='administrador', password='password123')
usuario3.groups.add(grupo_admin)

print("Grupos, permisos y usuarios creados exitosamente.")
Configuración adicional para el proyecto
Actualizar las vistas:

Los permission_required en las vistas deben coincidir con los permisos personalizados (crear_perm, ver_perm, borrar_perm).
Migraciones:

Ejecuta las migraciones antes de usar el script:
bash
Copiar código
python manage.py makemigrations
python manage.py migrate
Prueba de usuarios:

Inicia sesión con los usuarios creados y verifica que los permisos se apliquen correctamente. Por ejemplo:
Usuario creador: Solo puede crear mensajes.
Usuario editor: Solo puede ver y eliminar mensajes.
Usuario administrador: Puede crear, ver y eliminar mensajes.
