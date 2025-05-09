# Generated by Django 5.2 on 2025-04-10 11:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Il',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad', models.CharField(max_length=100, verbose_name='İl Adı')),
                ('slug', models.SlugField(blank=True, max_length=100, null=True, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'İl',
                'verbose_name_plural': 'İller',
                'ordering': ['ad'],
            },
        ),
        migrations.CreateModel(
            name='Meslek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad', models.CharField(max_length=100, verbose_name='Meslek Adı')),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True, verbose_name='Slug')),
                ('aciklama', models.TextField(blank=True, null=True, verbose_name='Açıklama')),
            ],
            options={
                'verbose_name': 'Meslek',
                'verbose_name_plural': 'Meslekler',
                'ordering': ['ad'],
            },
        ),
        migrations.CreateModel(
            name='Sektor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad', models.CharField(max_length=100, verbose_name='Sektör Adı')),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True, verbose_name='Slug')),
                ('aciklama', models.TextField(blank=True, null=True, verbose_name='Açıklama')),
            ],
            options={
                'verbose_name': 'Sektör',
                'verbose_name_plural': 'Sektörler',
                'ordering': ['ad'],
            },
        ),
        migrations.CreateModel(
            name='Ilce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad', models.CharField(max_length=100, verbose_name='İlçe Adı')),
                ('slug', models.SlugField(blank=True, max_length=150, null=True, verbose_name='Slug')),
                ('il', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ilceler', to='ayarlar.il', verbose_name='İl')),
            ],
            options={
                'verbose_name': 'İlçe',
                'verbose_name_plural': 'İlçeler',
                'ordering': ['ad'],
                'unique_together': {('il', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='Mahalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad', models.CharField(max_length=100, verbose_name='Mahalle Adı')),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, verbose_name='Slug')),
                ('ilce', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mahalleler', to='ayarlar.ilce', verbose_name='İlçe')),
            ],
            options={
                'verbose_name': 'Mahalle',
                'verbose_name_plural': 'Mahalleler',
                'ordering': ['ad'],
                'unique_together': {('ilce', 'slug')},
            },
        ),
    ]
