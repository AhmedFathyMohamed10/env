# Generated by Django 4.1.1 on 2022-09-14 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_customer_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='images/profile1.png', null=True, upload_to='profile_pics'),
        ),
    ]
