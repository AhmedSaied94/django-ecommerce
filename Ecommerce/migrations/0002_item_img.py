# Generated by Django 4.0.1 on 2022-01-09 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='items/imgs'),
        ),
    ]
