# Generated by Django 3.1.1 on 2020-10-08 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('city', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city.city')),
            ],
        ),
    ]
