# Generated by Django 3.2.3 on 2021-06-05 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('COMPLETED', 'Completed'), ('CANCELED', 'Canceled'), ('SUSPENDED', 'Suspended')], default='ACTIVE', help_text='وضعیت سفارش', max_length=100, verbose_name='Status'),
        ),
    ]
