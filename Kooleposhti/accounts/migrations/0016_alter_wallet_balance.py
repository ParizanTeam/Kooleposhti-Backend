# Generated by Django 3.2.8 on 2021-12-23 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=12),
        ),
    ]
