# Generated by Django 5.0.6 on 2024-06-25 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0003_producto_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='tipo',
            field=models.CharField(choices=[('Destilado', 'Destilado'), ('Licor', 'Licor'), ('Cerveza', 'Cerveza'), ('Whisky', 'Whisky'), ('Vino', 'Vino'), ('Espumante', 'Espumante')], default='destilado', max_length=20),
        ),
    ]
