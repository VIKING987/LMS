# Generated by Django 4.0 on 2021-12-26 18:51

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('libManager', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookrecords',
            name='is_Fiction',
        ),
        migrations.AddField(
            model_name='bookrecords',
            name='tags',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Drama', 'Drama'), ('Romance', 'Romance'), ('Thriller', 'Thriller'), ('Mystery', 'Mystery'), ('Comedy', 'Comedy'), ('Tragedy', 'Tragedy'), ('Autobiography', 'Autobiography'), ('Biography', 'Biography'), ('General-Knowledge', 'General-Knowledge')], default=None, max_length=87, verbose_name='Genre'),
        ),
        migrations.AlterField(
            model_name='bookrecords',
            name='copies_tot',
            field=models.IntegerField(verbose_name='Total Copies'),
        ),
        migrations.AlterField(
            model_name='bookrecords',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Title'),
        ),
    ]
