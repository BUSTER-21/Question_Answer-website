# Generated by Django 2.2.7 on 2019-11-10 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description_img',
            field=models.ImageField(default='blog/jammu.jpeg', upload_to='blog/'),
        ),
    ]