# Generated by Django 5.0.4 on 2024-05-04 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_topic_alter_phrase_embedding_alter_phrase_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='answer',
            field=models.TextField(max_length=3000),
        ),
    ]