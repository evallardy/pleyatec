# Generated by Django 4.0.4 on 2022-06-02 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bien', '0007_alter_lote_altura_alter_lote_esquina_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lote',
            name='gran_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Total gral.'),
        ),
    ]