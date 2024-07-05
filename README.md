## Viene con una base de datos lista para visualizar las funciones de la pagina.

#### Cuenta de usuario para testeo
##### user@user.com
##### testuser

#### Cuenta de Staff para testeo
##### staff@example.com
##### staffpw


### Hacer un usuario staff

__python manage.py shell__

```
from aplicacion.models import Usuario
from django.utils import timezone

Usuario.objects.create_staff_user(
email='staff@example.com',
rut='12345678-9',
nombre='Staff',
apellido='Staff',
telefono='987654321',
fecha_nacimiento=timezone.now(),
password='staffpw')
```
