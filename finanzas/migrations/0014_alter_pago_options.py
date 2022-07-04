# Generated by Django 4.0.4 on 2022-07-02 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0013_alter_pago_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pago',
            options={'ordering': ['id'], 'permissions': (('nuvole_estado_cuenta', 'Nuvole Mostrar estado de cuenta'), ('nuvole_listado_pagos', 'Nuvole Mostrar listado de pagos'), ('nuvole_comprobante_pagos', 'Nuvole Incluir comprobante de pago'), ('nuvole_confirma', 'Nuvole Confirma depósitos'), ('toscana_estado_cuenta', 'Toscana Mostrar estado de cuenta'), ('toscana_listado_pagos', 'Toscana Mostrar listado de pagos'), ('toscana_comprobante_pagos', 'Toscana Incluir comprobante de pago'), ('toscana_confirma', 'Toscana Confirma depósitos'), ('local_punta_o_estado_cuenta', 'Local Punta O Mostrar estado de cuenta'), ('local_punta_o_listado_pagos', 'Local Punta O Mostrar listado de pagos'), ('local_punta_o_comprobante_pagos', 'Local Punta O Incluir comprobante de pago'), ('local_punta_o_confirma', 'Local Punta O Confirma depósitos'), ('consul_punta_o_estado_cuenta', 'Consultorio Punta O Mostrar estado de cuenta'), ('consul_punta_o_listado_pagos', 'Consultorio Punta O Mostrar listado de pagos'), ('consul_punta_o_comprobante_pagos', 'Consultorio Punta O Incluir comprobante de pago'), ('consul_punta_o_confirma', 'Consultorio Punta O Confirma depósitos'), ('torre_vento_estado_cuenta', 'Torre Vento Mostrar estado de cuenta'), ('torre_vento_listado_pagos', 'Torre Vento Mostrar listado de pagos'), ('torre_vento_comprobante_pagos', 'Torre Vento Incluir comprobante de pago'), ('torre_vento_confirma', 'Torre Vento Confirma depósitos'), ('fraccion34_estado_cuenta', 'Fracción 34 Mostrar estado de cuenta'), ('fraccion34_listado_pagos', 'Fracción 34 Mostrar listado de pagos'), ('fraccion34_comprobante_pagos', 'Fracción 34 Incluir comprobante de pago'), ('fraccion34_confirma', 'Fracción 34 Confirma depósitos'), ('vivienda_nuvole_estado_cuenta', 'Vivienda Nuvole Mostrar estado de cuenta'), ('vivienda_nuvole_listado_pagos', 'Vivienda Nuvole Mostrar listado de pagos'), ('vivienda_nuvole_comprobante_pagos', 'Vivienda Nuvole Incluir comprobante de pago'), ('vivienda_nuvole_confirma', 'Vivienda Nuvole Confirma depósitos'), ('pathe_estado_cuenta', 'Pathe Mostrar estado de cuenta'), ('pathe_listado_pagos', 'Pathe Mostrar listado de pagos'), ('pathe_comprobante_pagos', 'Pathe Incluir comprobante de pago'), ('pathe_confirma', 'Pathe Confirma depósitos'), ('condom_multiple_estado_cuenta', 'Condominio Múltiple Mostrar estado de cuenta'), ('condom_multiple_listado_pagos', 'Condominio Múltiple Mostrar listado de pagos'), ('condom_multiple_comprobante_pagos', 'Condominio Múltiple Incluir comprobante de pago'), ('condom_multiple_confirma', 'Condominio Múltiple Confirma depósitos')), 'verbose_name': 'Pagos', 'verbose_name_plural': 'Pago'},
        ),
    ]