# Generated by Django 4.0 on 2021-12-26 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libManager', '0002_remove_bookrecords_is_fiction_bookrecords_tags_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookrecords',
            name='copies_tot',
        ),
        migrations.AlterField(
            model_name='bookrecords',
            name='copies_avail',
            field=models.IntegerField(default=1, verbose_name='Available Copies'),
        ),
    ]
