# Generated by Django 5.0.6 on 2024-07-23 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audiosity_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('description', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]