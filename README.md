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
    password='staffpw'
 )
```
