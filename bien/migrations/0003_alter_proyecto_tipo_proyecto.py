# Generated by Django 4.0.4 on 2022-06-02 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bien', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='tipo_proyecto',
            field=models.IntegerField(choices=[(1, 'Lotes'), (2, 'Locales comerciales'), (3, 'Vivienda horizontal'), (4, 'Vivienda vertical'), (5, 'Consultorios'), (6, 'Locales comerciales y oficinas')], default=1, verbose_name='Tipo de proyecto'),
        ),
    ]
