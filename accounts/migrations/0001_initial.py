# Generated by Django 5.1.3 on 2024-11-27 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.TextField(db_column='USERNAME')),
                ('password', models.TextField(db_column='PASSWORD')),
            ],
            options={
                'db_table': 'Accounts',
                'ordering': ['id'],
                'managed': True,
            },
        ),
    ]
