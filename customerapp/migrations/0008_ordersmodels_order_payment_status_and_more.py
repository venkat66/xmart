# Generated by Django 4.0.6 on 2022-08-02 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customerapp', '0007_rename_order_owner_ordersmodels_order_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordersmodels',
            name='order_payment_status',
            field=models.CharField(default='Pending', help_text='payment_status', max_length=20),
        ),
        migrations.AlterField(
            model_name='ordersmodels',
            name='order_status',
            field=models.CharField(default='Pending', help_text='order_status', max_length=100),
        ),
    ]