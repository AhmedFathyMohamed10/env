# Generated by Django 4.1.1 on 2022-10-08 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_customer_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='product_pics/default.png', null=True, upload_to='product_pics'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='profile_pics/profile1.png', null=True, upload_to='profile_pics'),
        ),
    ]