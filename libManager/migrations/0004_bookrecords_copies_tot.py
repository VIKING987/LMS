# Generated by Django 4.0 on 2021-12-27 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libManager', '0003_remove_bookrecords_copies_tot_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookrecords',
            name='copies_tot',
            field=models.IntegerField(default=None),
        ),
    ]
