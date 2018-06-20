# Generated by Django 2.0.6 on 2018-06-17 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inne_dania',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('overall_rate', models.IntegerField(default=0)),
                ('photo_ref', models.ImageField(default='no.png', upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Kebaby_dania',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('meat', models.IntegerField(default=0)),
                ('sauce', models.IntegerField(default=0)),
                ('batter', models.IntegerField(default=0)),
                ('salds', models.IntegerField(default=0)),
                ('photo_ref', models.ImageField(default='no.png', upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Kebaby_lokale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('localization_x', models.CharField(max_length=100)),
                ('localization_y', models.CharField(max_length=100)),
                ('rate', models.FloatField(default=0)),
                ('photo_ref', models.ImageField(default='no.png', upload_to='')),
            ],
        ),
        migrations.AddField(
            model_name='kebaby_dania',
            name='local_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kebab.Kebaby_lokale'),
        ),
        migrations.AddField(
            model_name='inne_dania',
            name='local_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kebab.Kebaby_lokale'),
        ),
    ]
