# Generated by Django 4.2.5 on 2023-09-27 07:05

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('product', '0005_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]