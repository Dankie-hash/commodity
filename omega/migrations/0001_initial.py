# Generated by Django 3.2.3 on 2021-05-28 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('current_price', models.FloatField()),
                ('opening_price', models.FloatField()),
                ('available', models.BooleanField()),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('unit', models.CharField(max_length=150)),
                ('volume', models.FloatField()),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to='commodities/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='omega.category')),
            ],
        ),
    ]
