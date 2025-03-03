# Generated by Django 5.1.5 on 2025-02-08 07:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_comment_reply'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postlike', to='home.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userlike', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
