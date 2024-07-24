# Generated by Django 5.0.6 on 2024-07-23 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audiosity_app', '0002_imagemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.DeleteModel(
            name='ImageModel',
        ),
    ]
