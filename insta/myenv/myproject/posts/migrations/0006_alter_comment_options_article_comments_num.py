# Generated by Django 4.2.4 on 2023-08-26 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_article_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created_at']},
        ),
        migrations.AddField(
            model_name='article',
            name='comments_num',
            field=models.IntegerField(default=0),
        ),
    ]
