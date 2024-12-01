# Generated by Django 5.1.1 on 2024-11-30 20:29

import django.core.files.storage
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Livro',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(help_text='nome', max_length=100)),
                ('categoria', models.CharField(choices=[('A', 'Autoajuda'), ('B', 'Bibliografia'), ('C', 'Comedia'), ('E', 'Epico'), ('I', 'Infantil'), ('L', 'Literatura'), ('M', 'Matematica'), ('P', 'Poesia'), ('R', 'Romance'), ('T', 'Terror')], default='SELECIONE', max_length=1)),
                ('capa', models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='VersoLivro/static/img/VersoLivro'), upload_to='')),
                ('sinopse', models.TextField(default='Sinopse..')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]