# Generated by Django 4.2.4 on 2023-09-02 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_comment_profile_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_at']},
        ),
    ]