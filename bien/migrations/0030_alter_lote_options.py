# Generated by Django 4.0.4 on 2022-07-13 01:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bien', '0029_alter_proyecto_nom_proy'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lote',
            options={'ordering': ['proyecto', 'lote'], 'permissions': (('nuvole_ver', 'Nuvole ver bienes'), ('nuvole_add', 'Nuvole agregar bien'), ('nuvole_chag', 'Nuvole cambiar bien'), ('nuvole_reservar', 'Nuvole reservar bien'), ('toscana_ver', 'Toscana ver bienes'), ('toscana_add', 'Toscana agregar bien'), ('toscana_chag', 'Toscana cambiar bien'), ('toscana_reservar', 'Toscana reservar bien'), ('local_punta_o_ver', 'Punta O local ver bienes'), ('local_punta_o_add', 'Punta O local agregar bien'), ('local_punta_o_chag', 'Punta O local cambiar bien'), ('local_punta_o_reservar', 'Punta O local reservar bien'), ('consul_punta_o_ver', 'Punta O consult ver bienes'), ('consul_punta_o_add', 'Punta O consult agregar bien'), ('consul_punta_o_chag', 'Punta O consult cambiar bien'), ('consul_punta_o_reservar', 'Punta O consult reservar bien'), ('torre_vento_ver', 'Torre Vento ver bienes'), ('torre_vento_add', 'Torre Vento agregar bien'), ('torre_vento_chag', 'Torre Vento cambiar bien'), ('torre_vento_reservar', 'Torre Vento reservar bien bien'), ('fraccion34_ver', 'Fracción 34 ver bienes'), ('fraccion34_add', 'Fracción 34 agregar bien'), ('fraccion34_chag', 'Fracción 34 cambiar bien'), ('fraccion34_reservar', 'Fracción 34 reservar bien'), ('vivienda_nuvole_ver', 'Nuvole viviendas ver bienes'), ('vivienda_nuvole_add', 'Nuvole viviendas agregar bien'), ('vivienda_nuvole_chag', ' Nuvole viviendas cambiar bien'), ('vivienda_nuvole_reservar', 'Nuvole viviendas reservar bien'), ('pathe_ver', 'Pathe ver bienes'), ('pathe_add', 'Pathe agregar bien'), ('pathe_chag', 'Pathe cambiar bien'), ('pathe_reservar', 'Pathe reservar bien'), ('condom_multiple_ver', 'Condominio Múltiple ver bienes'), ('condom_multiple_add', 'Condominio Múltiple agregar bien'), ('condom_multiple_chag', 'Condominio Múltiple cambiar bien'), ('condom_multiple_reservar', 'Condominio Múltiple reservar bien')), 'verbose_name': 'Lote', 'verbose_name_plural': 'Lotes'},
        ),
    ]
