# Generated by Django 3.1.1 on 2020-09-22 19:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brewery',
            name='user',
        ),
        migrations.AddField(
            model_name='brewery',
            name='api_id',
            field=models.IntegerField(default=0, max_length=10),
        ),
        migrations.AddField(
            model_name='brewery',
            name='country',
            field=models.CharField(default='United States', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brewery',
            name='latitude',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brewery',
            name='longitude',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brewery',
            name='phone',
            field=models.CharField(default='000-000-0000', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brewery',
            name='postal_code',
            field=models.CharField(default='00000-0000', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brewery',
            name='street',
            field=models.CharField(default='0000', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brewery',
            name='website_url',
            field=models.CharField(default='www.brewsky.com', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='brewery',
            name='state',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=200)),
                ('brewery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.brewery')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
