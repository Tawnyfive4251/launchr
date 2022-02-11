# Generated by Django 3.2.11 on 2022-01-27 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AudioDataModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_file', models.FileField(upload_to='')),
                ('exported_file_name', models.TextField(blank=True, null=True)),
                ('transcript', models.TextField(blank=True, null=True)),
                ('error_occurred', models.BooleanField(default=False)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PEN', 'Pending'), ('COM', 'Complete'), ('ERR', 'Error')], default='PEN', max_length=3)),
                ('time_taken', models.DurationField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
    ]
