# Generated by Django 2.2.12 on 2021-02-19 19:22

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('public_covid', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='disclose',
            field=otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], null=True, verbose_name='Do you want to disclose your type to the other player?'),
        ),
    ]
