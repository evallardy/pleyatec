# Generated by Django 3.2.4 on 2022-07-31 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empleado', '0003_auto_20220731_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='genero',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], default='M', max_length=1, verbose_name='Género'),
        ),
    ]
