# Generated by Django 3.2.10 on 2021-12-17 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('param', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='param',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
