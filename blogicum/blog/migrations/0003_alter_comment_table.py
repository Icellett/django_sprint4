# Generated by Django 3.2.16 on 2025-01-09 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20250108_1431'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='comment',
            table='blog_comment',
        ),
    ]
