# Generated by Django 4.2.4 on 2023-10-02 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0023_remove_article_images_article_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='video',
            field=models.ManyToManyField(blank=True, null=True, to='posts.video'),
        ),
    ]