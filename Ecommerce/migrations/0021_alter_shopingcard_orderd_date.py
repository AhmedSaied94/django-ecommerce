# Generated by Django 4.0.1 on 2022-01-24 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerce', '0020_rename_ammount_payment_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopingcard',
            name='orderd_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]