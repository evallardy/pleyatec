# Generated by Django 3.2.4 on 2022-07-31 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bien', '0038_auto_20220731_0257'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proyecto',
            options={'ordering': ['id'], 'permissions': (('nuvole_acceso', 'Nuvole Acceso'), ('toscana_acceso', 'Toscana Acceso'), ('local_punta_o_acceso', 'Local Punta O Acceso'), ('consul_punta_o_acceso', 'Consultorio Punta O Acceso'), ('torre_vento_acceso', 'Torre Vento Acceso'), ('fraccion34_acceso', 'Fracción 34 Acceso'), ('vivienda_nuvole_acceso', 'Vivienda Nuvole Acceso'), ('pathe_acceso', 'Pathe Acceso'), ('condom_multiple_acceso', 'Condominio Múltiple Acceso'), ('comision_proyectos', 'Comisiones por proyecto')), 'verbose_name': 'Proyecto', 'verbose_name_plural': 'Proyectos'},
        ),
    ]