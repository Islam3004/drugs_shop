# Generated by Django 3.2.9 on 2022-02-14 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20220214_1719'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subcategories',
            old_name='name',
            new_name='title',
        ),
    ]