# Generated by Django 5.2.1 on 2025-05-17 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='Listing_date',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='square_feet',
        ),
        migrations.AlterField(
            model_name='listing',
            name='home_type',
            field=models.CharField(choices=[('HOUSE', 'House'), ('CONDO', 'Condo'), ('TOWNHOUSE', 'Townhouse')], default='HOUSE', max_length=10),
        ),
    ]
