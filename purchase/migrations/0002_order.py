# Generated by Django 3.2.15 on 2022-09-22 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField()),
                ('price', models.IntegerField(default=0)),
                ('items', models.ManyToManyField(related_name='order', to='purchase.Product')),
            ],
        ),
    ]
