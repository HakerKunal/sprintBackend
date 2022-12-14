# Generated by Django 2.1 on 2022-09-23 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sprint', '0002_auto_20220908_0521'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShowResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show', models.BooleanField(default=False)),
                ('sprint_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sprint.Sprint')),
            ],
        ),
    ]
