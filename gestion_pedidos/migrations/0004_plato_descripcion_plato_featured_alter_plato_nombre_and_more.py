# Generated by Django 5.0.7 on 2024-07-17 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_pedidos', '0003_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='plato',
            name='descripcion',
            field=models.TextField(default='Descripción no disponible'),
        ),
        migrations.AddField(
            model_name='plato',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='plato',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='plato',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
