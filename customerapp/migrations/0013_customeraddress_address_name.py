# Generated by Django 4.0.6 on 2022-08-03 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customerapp', '0012_rename_address_customeraddress_state_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeraddress',
            name='address_name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]