# Generated by Django 3.0.4 on 2020-04-06 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='profile_pic',
            field=models.ImageField(blank='True', upload_to='uploads/'),
        ),
    ]
