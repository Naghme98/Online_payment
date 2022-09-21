# Generated by Django 3.2.15 on 2022-09-20 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField()),
                ('price', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
    ]
