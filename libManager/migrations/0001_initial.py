# Generated by Django 4.0 on 2021-12-26 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookRecords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('copies_tot', models.IntegerField()),
                ('copies_avail', models.IntegerField()),
                ('is_Fiction', models.BooleanField(default=False)),
            ],
        ),
    ]