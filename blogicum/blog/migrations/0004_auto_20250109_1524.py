# Generated by Django 3.2.16 on 2025-01-09 09:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_alter_comment_table'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'default_related_name': 'comments', 'ordering': ('created_at',), 'verbose_name': 'комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='content',
            new_name='text',
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Добавлено'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post', verbose_name='Комментарий'),
        ),
        migrations.AlterModelTable(
            name='comment',
            table=None,
        ),
    ]
