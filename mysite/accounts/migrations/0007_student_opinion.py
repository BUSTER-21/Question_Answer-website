# Generated by Django 2.2.7 on 2019-11-10 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_student_describe_yourself'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='opinion',
            field=models.TextField(blank=True, default='No matter what your dream , it will come true.', help_text='know your opnion', max_length=255),
        ),
    ]
