# Generated by Django 4.0.4 on 2022-05-31 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('empleado', '0001_initial'),
        ('bien', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='usuario_ins',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='py_user_ins', to='empleado.empleado', verbose_name='Usuario insertó'),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='usuario_mod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='py_user_mod', to='empleado.empleado', verbose_name='Usuario modificó'),
        ),
        migrations.AddField(
            model_name='lote',
            name='asesor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='empleado.empleado', verbose_name='Asesor'),
        ),
        migrations.AddField(
            model_name='lote',
            name='proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bien.proyecto', verbose_name='Proyecto'),
        ),
        migrations.AddField(
            model_name='estacionamiento',
            name='lote',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bien.lote', verbose_name='Departamento'),
        ),
        migrations.AddField(
            model_name='esquema',
            name='proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bien.proyecto', verbose_name='PlanoProyecto'),
        ),
        migrations.AlterUniqueTogether(
            name='lote',
            unique_together={('proyecto', 'fase', 'manzana', 'lote')},
        ),
        migrations.AlterUniqueTogether(
            name='estacionamiento',
            unique_together={('lote', 'numero')},
        ),
        migrations.AlterUniqueTogether(
            name='esquema',
            unique_together={('proyecto', 'nombre_plano')},
        ),
    ]
